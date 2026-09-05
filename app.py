import os
import uuid
import base64
import json
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from google import genai
from google.genai import types
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Max 5MB upload
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Gemini API Setup
# Source: ai.google.dev/pricing (updated 2026-09-04)
# gemini-3.8-flash     = latest Flash model, current default in Google AI Studio (Sept 2026)
# gemini-3.5-flash-lite = lightweight fallback, also on free tier
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_FALLBACK_MODEL = "gemini-3.5-flash-lite"

gemini_client = None
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    print("Gemini client initialized. Primary model: " + GEMINI_MODEL)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

# Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Supabase error: " + str(e))
else:
    print("WARNING: SUPABASE credentials not found in environment variables.")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def analyze_crop_image(image_bytes, mime_type):
    prompt = (
        "Analyze this crop leaf image and identify any disease present.\n\n"
        "Return STRICTLY a JSON object with these exact keys:\n"
        '{ "crop_name": "name of the crop (e.g. Tomato, Rice, Wheat)",\n'
        '  "disease_name": "disease name or Healthy if none",\n'
        '  "severity": "mild | moderate | severe | N/A",\n'
        '  "cause": "pathogen or N/A if healthy",\n'
        '  "treatment": "recommended treatment or N/A if healthy" }\n\n'
        "Output ONLY raw JSON. No markdown, no code fences, no extra text."
    )
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    text_part = types.Part.from_text(text=prompt)
    models_to_try = [GEMINI_MODEL, GEMINI_FALLBACK_MODEL]
    last_error = None
    for model_name in models_to_try:
        try:
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=[types.Content(role="user", parts=[image_part, text_part])],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            raw = response.text.strip()
            print("Gemini [" + model_name + "]: " + raw[:200])
            return raw, model_name
        except Exception as e:
            es = str(e)
            print("Gemini [" + model_name + "] error: " + es)
            if "403" in es or "PERMISSION_DENIED" in es or "permission" in es.lower():
                last_error = e
                continue
            raise e
    raise Exception("All Gemini models failed. Last error: " + str(last_error))


def parse_gemini_json(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)


def upload_image_to_supabase(image_bytes, filename, mime_type):
    if not supabase:
        return None
    try:
        try:
            supabase.storage.create_bucket("crop-images", options={"public": True})
        except Exception:
            pass
        bucket = supabase.storage.from_("crop-images")
        bucket.upload(path=filename, file=image_bytes, file_options={"content-type": mime_type})
        return bucket.get_public_url(filename)
    except Exception as e:
        print("Supabase upload failed: " + str(e))
        return None


@app.route("/")
def index():
    return render_template("index.html", user_email=session.get("user_email"))

@app.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("analyze"))
    return render_template("login.html")

@app.route("/signup")
def signup():
    if session.get("user_id"):
        return redirect(url_for("analyze"))
    return render_template("signup.html")

@app.route("/analyze")
@login_required
def analyze():
    return render_template("analyze.html", user_email=session.get("user_email"))

@app.route("/result")
@login_required
def result():
    return render_template("result.html", user_email=session.get("user_email"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user_email=session.get("user_email"))


@app.route("/auth/signup", methods=["POST"])
def auth_signup():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if not supabase:
        return jsonify({"error": "Auth service not configured."}), 500
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": name}}
        })
        user = response.user
        if not user:
            return jsonify({"error": "Sign-up failed. Email may already be registered."}), 400
        session["user_id"] = user.id
        session["user_email"] = user.email
        return jsonify({"success": True, "redirect": "/analyze"})
    except Exception as e:
        em = str(e)
        if "already registered" in em.lower():
            return jsonify({"error": "Email already registered. Please log in."}), 400
        return jsonify({"error": "Sign-up failed: " + em}), 500


@app.route("/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if not supabase:
        return jsonify({"error": "Auth service not configured."}), 500
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        if not user:
            return jsonify({"error": "Invalid email or password."}), 401
        session["user_id"] = user.id
        session["user_email"] = user.email
        return jsonify({"success": True, "redirect": "/analyze"})
    except Exception as e:
        em = str(e)
        if "invalid" in em.lower() or "credentials" in em.lower():
            return jsonify({"error": "Invalid email or password."}), 401
        return jsonify({"error": "Login failed: " + em}), 500


@app.route("/auth/logout")
def auth_logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/detect", methods=["POST"])
@login_required
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400
    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No image selected."}), 400
    if image_file.content_type not in ALLOWED_MIME_TYPES:
        return jsonify({"error": "Only JPEG, PNG, and WebP images are supported."}), 400
    if not gemini_client:
        return jsonify({"error": "Gemini API not configured on server."}), 500
    try:
        image_bytes = image_file.read()
        mime_type = image_file.content_type or "image/jpeg"
        raw_text, used_model = analyze_crop_image(image_bytes, mime_type)
        print("Analysis complete using: " + used_model)
        try:
            analysis_result = parse_gemini_json(raw_text)
        except json.JSONDecodeError as json_err:
            print("JSON error: " + str(json_err) + "\nRaw: " + raw_text)
            return jsonify({"error": "AI returned invalid JSON. Raw: " + raw_text[:300]}), 500
        for key in ["crop_name", "disease_name", "severity", "cause", "treatment"]:
            if key not in analysis_result:
                analysis_result[key] = "Unknown"
        file_ext = image_file.filename.rsplit(".", 1)[-1] if "." in image_file.filename else "jpg"
        unique_filename = "scan_" + uuid.uuid4().hex + "." + file_ext
        image_url = upload_image_to_supabase(image_bytes, unique_filename, mime_type)
        if not image_url:
            enc = base64.b64encode(image_bytes).decode("utf-8")
            image_url = "data:" + mime_type + ";base64," + enc
        analysis_result["image_url"] = image_url
        return jsonify(analysis_result)
    except Exception as e:
        em = str(e)
        print("Detection error: " + em)
        if "403" in em or "PERMISSION_DENIED" in em:
            return jsonify({"error": "API access denied (403). Regenerate your key at aistudio.google.com/apikey and update it in Vercel."}), 503
        elif "quota" in em.lower() or "rate" in em.lower():
            return jsonify({"error": "Rate limit exceeded. Please wait and try again."}), 429
        return jsonify({"error": "Analysis failed: " + em}), 500


@app.route("/history", methods=["GET"])
@login_required
def history():
    if not supabase:
        return jsonify({"error": "Supabase not configured."}), 500
    user_id = session.get("user_id")
    try:
        response = (
            supabase.table("scans")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": "Failed to retrieve history: " + str(e)}), 500


@app.route("/save", methods=["POST"])
@login_required
def save():
    if not supabase:
        return jsonify({"error": "Supabase not configured."}), 500
    data = request.json or request.form
    if not data:
        return jsonify({"error": "No scan data provided."}), 400
    for field in ["crop_name", "disease_name", "severity", "treatment"]:
        if not data.get(field):
            return jsonify({"error": "Missing required field: " + field}), 400
    try:
        insert_data = {
            "user_id": session.get("user_id"),
            "crop_name": data.get("crop_name"),
            "disease_name": data.get("disease_name"),
            "severity": data.get("severity"),
            "cause": data.get("cause", "N/A"),
            "treatment": data.get("treatment"),
            "image_url": data.get("image_url", "")
        }
        response = supabase.table("scans").insert(insert_data).execute()
        return jsonify({"success": True, "data": response.data[0] if response.data else insert_data})
    except Exception as e:
        return jsonify({"error": "Failed to save scan: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, port=int(os.getenv("PORT", 5000)))

# Required by Vercel / Gunicorn WSGI
application = app

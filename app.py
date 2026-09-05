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
# File upload security
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Max 5MB upload
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

# Configure Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
else:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")

# ── Auth decorator ────────────────────────────────────────────────────────────
def login_required(f):
    """Redirect to /login if the user has no active session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ── Image upload helper ───────────────────────────────────────────────────────
def upload_image_to_supabase(image_bytes, filename, mime_type):
    """
    Attempts to upload the scan image to Supabase Storage bucket 'crop-images'.
    Returns the public URL if successful, otherwise None.
    """
    if not supabase:
        return None
    try:
        try:
            supabase.storage.create_bucket("crop-images", options={"public": True})
        except Exception:
            pass

        bucket = supabase.storage.from_("crop-images")
        bucket.upload(
            path=filename,
            file=image_bytes,
            file_options={"content-type": mime_type}
        )
        public_url = bucket.get_public_url(filename)
        return public_url
    except Exception as e:
        print(f"Failed to upload image to Supabase Storage: {e}")
        return None

# ── Public page routes ────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', user_email=session.get("user_email"))

@app.route('/login')
def login():
    if session.get("user_id"):
        return redirect(url_for("analyze"))
    return render_template('login.html')

@app.route('/signup')
def signup():
    if session.get("user_id"):
        return redirect(url_for("analyze"))
    return render_template('signup.html')

# ── Protected page routes ─────────────────────────────────────────────────────
@app.route('/analyze')
@login_required
def analyze():
    return render_template('analyze.html', user_email=session.get("user_email"))

@app.route('/result')
@login_required
def result():
    return render_template('result.html', user_email=session.get("user_email"))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_email=session.get("user_email"))

# ── Auth API routes ───────────────────────────────────────────────────────────
@app.route('/auth/signup', methods=['POST'])
def auth_signup():
    """Create a new Supabase Auth user and log them in."""
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if not supabase:
        return jsonify({"error": "Authentication service is not configured."}), 500

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"full_name": name}
            }
        })

        user = response.user
        if not user:
            return jsonify({"error": "Sign-up failed. The email may already be registered."}), 400

        session["user_id"] = user.id
        session["user_email"] = user.email

        return jsonify({"success": True, "redirect": "/analyze"})

    except Exception as e:
        error_msg = str(e)
        print(f"Sign-up error: {error_msg}")
        if "already registered" in error_msg.lower() or "already been registered" in error_msg.lower():
            return jsonify({"error": "This email is already registered. Please log in instead."}), 400
        return jsonify({"error": f"Sign-up failed: {error_msg}"}), 500


@app.route('/auth/login', methods=['POST'])
def auth_login():
    """Authenticate an existing Supabase Auth user and create a session."""
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if not supabase:
        return jsonify({"error": "Authentication service is not configured."}), 500

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = response.user
        if not user:
            return jsonify({"error": "Invalid email or password."}), 401

        session["user_id"] = user.id
        session["user_email"] = user.email

        return jsonify({"success": True, "redirect": "/analyze"})

    except Exception as e:
        error_msg = str(e)
        print(f"Login error: {error_msg}")
        if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
            return jsonify({"error": "Invalid email or password."}), 401
        return jsonify({"error": f"Login failed: {error_msg}"}), 500


@app.route('/auth/logout')
def auth_logout():
    """Clear the Flask session and redirect to login."""
    session.clear()
    return redirect(url_for("login"))

# ── Protected API routes ──────────────────────────────────────────────────────
@app.route('/detect', methods=['POST'])
@login_required
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided in request."}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "No image selected for uploading."}), 400

    if image_file.content_type not in ALLOWED_MIME_TYPES:
        return jsonify({"error": "Only JPEG, PNG, and WebP images are supported."}), 400

    try:
        image_bytes = image_file.read()
        mime_type = image_file.content_type or 'image/jpeg'

        if not GEMINI_API_KEY:
            return jsonify({"error": "Gemini API is not configured on the server."}), 500

        prompt = """
        Analyze this crop leaf image. Identify:
        1. Crop Name
        2. Disease Name (or "Healthy" if no disease is found)
        3. Severity (must be one of: mild, moderate, severe, or "N/A" if healthy)
        4. Cause of the disease (or "N/A" if healthy)
        5. Treatment recommendation (or "N/A" if healthy)

        Return the response STRICTLY as a JSON object with these exact keys:
        {
          "crop_name": "...",
          "disease_name": "...",
          "severity": "...",
          "cause": "...",
          "treatment": "..."
        }
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        types.Part.from_text(text=prompt)
                    ]
                )
            ]
        )

        result_text = response.text
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("\n", 1)[-1]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text.rsplit("```", 1)[0].strip()

        try:
            analysis_result = json.loads(cleaned_text)
        except json.JSONDecodeError as json_err:
            print(f"JSON parse error: {json_err}")
            print(f"Raw Gemini response:\n{result_text}")
            return jsonify({"error": f"Failed to parse Gemini response as JSON: {str(json_err)}"}), 500

        file_ext = image_file.filename.split('.')[-1] if '.' in image_file.filename else 'jpg'
        unique_filename = f"scan_{uuid.uuid4().hex}.{file_ext}"

        image_url = upload_image_to_supabase(image_bytes, unique_filename, mime_type)
        if not image_url:
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:{mime_type};base64,{encoded_image}"

        analysis_result["image_url"] = image_url

        return jsonify(analysis_result)

    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500


@app.route('/history', methods=['GET'])
@login_required
def history():
    if not supabase:
        return jsonify({"error": "Supabase connection is not configured."}), 500

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
        print(f"Error fetching history: {e}")
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500


@app.route('/save', methods=['POST'])
@login_required
def save():
    if not supabase:
        return jsonify({"error": "Supabase connection is not configured."}), 500

    data = request.json or request.form
    if not data:
        return jsonify({"error": "No scan data provided."}), 400

    required_fields = ["crop_name", "disease_name", "severity", "treatment"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

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
        print(f"Error saving scan: {e}")
        return jsonify({"error": f"Failed to save scan record: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=False, port=int(os.getenv("PORT", 5000)))

application = app
            

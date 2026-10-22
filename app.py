import os
import traceback
import uuid
import base64
import json
from datetime import datetime, timezone
import requests
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Max 5MB upload
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# OpenRouter API Setup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")

if OPENROUTER_API_KEY:
    print("OpenRouter client ready. Model: " + OPENROUTER_MODEL)
else:
    print("WARNING: OPENROUTER_API_KEY not found in environment variables.")

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


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "bn": "Bengali",
    "ml": "Malayalam",
}


def analyze_crop_image(image_bytes, mime_type, language="en"):
    lang_name = SUPPORTED_LANGUAGES.get(language, "English")
    prompt = (
        f"Analyze this crop leaf image and identify any disease present.\n\n"
        f"Provide the analysis in {lang_name} ({language}) for disease_name, cause, treatment, organic_options, chemical_options, prevention_tips, safety_note, and retake_tip.\n"
        f"Return STRICTLY a JSON object with these exact keys:\n"
        '{\n'
        '  "crop_name": "name of the crop (e.g. Tomato, Rice, Wheat)",\n'
        f'  "disease_name": "disease name in {lang_name} or Healthy if none",\n'
        '  "disease_name_en": "disease name in English or Healthy if none",\n'
        '  "severity": "mild | moderate | severe | N/A",\n'
        f'  "cause": "pathogen/cause in {lang_name} or N/A if healthy",\n'
        f'  "treatment": "short combined treatment summary in {lang_name} or N/A if healthy",\n'
        f'  "organic_options": ["2 to 4 short organic/biological treatment methods in {lang_name}, or empty list [] if healthy"],\n'
        f'  "chemical_options": ["2 to 4 chemical options naming active ingredients or product classes (no brand names) in {lang_name}, or empty list [] if healthy"],\n'
        f'  "prevention_tips": ["2 to 3 practical prevention tips in {lang_name}"],\n'
        f'  "safety_note": "one sentence in {lang_name} regarding safety precautions (gloves, mask, label instructions, consulting local Krishi Vigyan Kendra)",\n'
        '  "confidence": integer 0-100 representing diagnostic confidence percentage,\n'
        '  "image_quality": "good | blurry | too_dark | not_a_leaf | multiple_leaves",\n'
        f'  "retake_tip": "one short sentence in {lang_name} with photography guidance if quality is not good or confidence is low, or advice to maintain crop health if good"\n'
        '}\n\n'
        'Important Instructions:\n'
        '- Do not invent exact chemical doses. Advise following the product label and consulting the local Krishi Vigyan Kendra before spraying.\n'
        '- "chemical_options" MUST name generic active ingredients or chemical classes (e.g., Mancozeb, Copper Oxychloride, Azoxystrobin, Chlorothalonil), NEVER proprietary brand names.\n'
        '- If the plant is Healthy, "organic_options" and "chemical_options" MUST be empty lists [].\n'
        '- "severity" MUST be one of: "mild", "moderate", "severe", "N/A" (exact English enum).\n'
        '- "image_quality" MUST be one of: "good", "blurry", "too_dark", "not_a_leaf", "multiple_leaves" (exact English enum).\n'
        '- "confidence" MUST be an integer between 0 and 100.\n'
        '- "disease_name_en" MUST be in English.\n'
        'Output ONLY raw JSON. No markdown, no code fences, no extra text.'
    )

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{encoded_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            },
            timeout=30
        )

        if response.status_code == 401:
            raise Exception("Invalid OpenRouter API key. Check OPENROUTER_API_KEY in Vercel.")
        elif response.status_code == 402:
            raise Exception("OpenRouter account has no credits. Add credits at openrouter.ai.")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded. Please wait and try again.")
        elif response.status_code != 200:
            raise Exception(f"OpenRouter API error {response.status_code}: {response.text[:200]}")

        raw = response.json()["choices"][0]["message"]["content"].strip()
        print("OpenRouter [" + OPENROUTER_MODEL + "]: " + raw[:200])
        return raw, OPENROUTER_MODEL

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except Exception as e:
        raise Exception("Analysis failed: " + str(e))


def parse_ai_json(raw_text):
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
        traceback.print_exc()
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
        traceback.print_exc()
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
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OpenRouter API not configured on server. Set OPENROUTER_API_KEY in Vercel environment variables."}), 500

    language = (request.form.get("language") or "en").strip().lower()
    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    try:
        image_bytes = image_file.read()
        mime_type = image_file.content_type or "image/jpeg"
        raw_text, used_model = analyze_crop_image(image_bytes, mime_type, language=language)
        print("Analysis complete using: " + used_model)
        try:
            analysis_result = parse_ai_json(raw_text)
        except json.JSONDecodeError as json_err:
            print("JSON error: " + str(json_err) + "\nRaw: " + raw_text)
            return jsonify({"error": "AI returned invalid JSON. Raw: " + raw_text[:300]}), 500
        for key in ["crop_name", "disease_name", "disease_name_en", "severity", "cause", "treatment"]:
            if key not in analysis_result:
                analysis_result[key] = "Unknown"
        if analysis_result.get("disease_name_en") in [None, "", "Unknown"]:
            analysis_result["disease_name_en"] = analysis_result.get("disease_name", "Unknown")

        # Parse organic_options, chemical_options, prevention_tips (must be lists of strings)
        def sanitize_string_list(val):
            if isinstance(val, list):
                return [str(item).strip() for item in val if str(item).strip()]
            elif isinstance(val, str) and val.strip():
                return [val.strip()]
            return []

        analysis_result["organic_options"] = sanitize_string_list(analysis_result.get("organic_options"))
        analysis_result["chemical_options"] = sanitize_string_list(analysis_result.get("chemical_options"))
        analysis_result["prevention_tips"] = sanitize_string_list(analysis_result.get("prevention_tips"))

        # Parse safety_note
        safety_note = str(analysis_result.get("safety_note") or "").strip()
        if not safety_note:
            safety_note = "Always wear protective gear (gloves, mask), follow product label instructions carefully, and consult your local Krishi Vigyan Kendra before spraying."
        analysis_result["safety_note"] = safety_note

        # Parse and sanitize confidence (integer 0-100)
        raw_conf = analysis_result.get("confidence")
        try:
            confidence = int(raw_conf)
            confidence = max(0, min(100, confidence))
        except (TypeError, ValueError):
            confidence = 75
        analysis_result["confidence"] = confidence

        # Parse and sanitize image_quality (good | blurry | too_dark | not_a_leaf | multiple_leaves)
        valid_qualities = {"good", "blurry", "too_dark", "not_a_leaf", "multiple_leaves"}
        img_quality = str(analysis_result.get("image_quality", "good")).strip().lower()
        if img_quality not in valid_qualities:
            img_quality = "good"
        analysis_result["image_quality"] = img_quality

        # Parse retake_tip
        retake_tip = str(analysis_result.get("retake_tip") or "").strip()
        analysis_result["retake_tip"] = retake_tip

        # needs_retake boolean: true if image_quality != "good" or confidence < 60
        needs_retake = (img_quality != "good") or (confidence < 60)
        analysis_result["needs_retake"] = needs_retake

        file_ext = image_file.filename.rsplit(".", 1)[-1] if "." in image_file.filename else "jpg"
        unique_filename = "scan_" + uuid.uuid4().hex + "." + file_ext
        image_url = upload_image_to_supabase(image_bytes, unique_filename, mime_type)
        if not image_url:
            enc = base64.b64encode(image_bytes).decode("utf-8")
            image_url = "data:" + mime_type + ";base64," + enc
        analysis_result["image_url"] = image_url
        analysis_result["language"] = language
        return jsonify(analysis_result)
    except Exception as e:
        em = str(e)
        print("Detection error: " + em)
        if "401" in em or "invalid" in em.lower() and "api key" in em.lower():
            return jsonify({"error": "Invalid OpenRouter API key. Check OPENROUTER_API_KEY in Vercel."}), 503
        elif "429" in em or "rate" in em.lower():
            return jsonify({"error": "Rate limit exceeded. Please wait and try again."}), 429
        elif "402" in em or "credits" in em.lower():
            return jsonify({"error": "OpenRouter account has no credits. Add credits at openrouter.ai."}), 503
        return jsonify({"error": "Analysis failed: " + em}), 500


@app.route("/translate", methods=["POST"])
@login_required
def translate():
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OpenRouter API not configured on server. Set OPENROUTER_API_KEY in Vercel environment variables."}), 500

    data = request.get_json() or {}
    fields = data.get("fields") or {}
    target_lang = (data.get("language") or "").strip().lower()

    if target_lang not in SUPPORTED_LANGUAGES:
        return jsonify({"error": f"Unsupported language '{target_lang}'."}), 400

    if not isinstance(fields, dict):
        return jsonify({"error": "Invalid 'fields' payload; must be a JSON object."}), 400

    target_lang_name = SUPPORTED_LANGUAGES[target_lang]

    prompt = (
        f"Translate the following crop disease report fields into {target_lang_name} ({target_lang}).\n"
        f"Preserve technical accuracy and chemical active ingredient names.\n"
        f"Return STRICTLY a JSON object with these exact keys:\n"
        '{\n'
        f'  "disease_name": "translated disease name in {target_lang_name} or Healthy if healthy",\n'
        f'  "cause": "translated pathogen/cause in {target_lang_name} or N/A",\n'
        f'  "treatment": "translated treatment summary in {target_lang_name} or N/A",\n'
        f'  "organic_options": ["translated organic treatment options in {target_lang_name}"],\n'
        f'  "chemical_options": ["translated chemical treatment options in {target_lang_name}"],\n'
        f'  "prevention_tips": ["translated prevention tips in {target_lang_name}"],\n'
        f'  "safety_note": "translated safety note in {target_lang_name}",\n'
        f'  "retake_tip": "translated retake guidance in {target_lang_name} or empty string"\n'
        '}\n\n'
        f"Fields to translate:\n"
        f"{json.dumps(fields, ensure_ascii=False)}\n\n"
        "Output ONLY raw JSON. No markdown, no code fences, no extra text."
    )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=30
        )

        if response.status_code == 401:
            return jsonify({"error": "Invalid OpenRouter API key."}), 503
        elif response.status_code == 402:
            return jsonify({"error": "OpenRouter account has no credits."}), 503
        elif response.status_code == 429:
            return jsonify({"error": "Rate limit exceeded. Please wait and try again."}), 429
        elif response.status_code != 200:
            return jsonify({"error": f"OpenRouter API error {response.status_code}: {response.text[:200]}"}), 502

        raw = response.json()["choices"][0]["message"]["content"].strip()
        translated = parse_ai_json(raw)

        def sanitize_list(val, fallback):
            if isinstance(val, list):
                return [str(i).strip() for i in val if str(i).strip()]
            return fallback if isinstance(fallback, list) else []

        return jsonify({
            "disease_name": translated.get("disease_name", fields.get("disease_name", "")),
            "cause": translated.get("cause", fields.get("cause", "")),
            "treatment": translated.get("treatment", fields.get("treatment", "")),
            "organic_options": sanitize_list(translated.get("organic_options"), fields.get("organic_options", [])),
            "chemical_options": sanitize_list(translated.get("chemical_options"), fields.get("chemical_options", [])),
            "prevention_tips": sanitize_list(translated.get("prevention_tips"), fields.get("prevention_tips", [])),
            "safety_note": translated.get("safety_note", fields.get("safety_note", "")),
            "retake_tip": translated.get("retake_tip", fields.get("retake_tip", ""))
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Translation failed: " + str(e)}), 500


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


@app.route("/report/<int:scan_id>", methods=["GET"])
@login_required
def report(scan_id):
    if not supabase:
        return jsonify({"error": "Supabase not configured."}), 500
    user_id = session.get("user_id")
    user_email = session.get("user_email")
    try:
        response = (
            supabase.table("scans")
            .select("*")
            .eq("id", scan_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data or len(response.data) == 0:
            abort(404)
        scan = response.data[0]

        def parse_to_list(val):
            if isinstance(val, list):
                return val
            if isinstance(val, str) and val.strip():
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
                return [val.strip()]
            return []

        scan["organic_options"] = parse_to_list(scan.get("organic_options"))
        scan["chemical_options"] = parse_to_list(scan.get("chemical_options"))
        scan["prevention_tips"] = parse_to_list(scan.get("prevention_tips"))

        try:
            scan["confidence"] = int(scan.get("confidence") or 75)
        except (ValueError, TypeError):
            scan["confidence"] = 75

        return render_template("report.html", scan=scan, user_email=user_email)
    except Exception as e:
        if hasattr(e, "code") and e.code == 404:
            raise e
        return jsonify({"error": "Failed to retrieve report: " + str(e)}), 500


@app.route("/scans/<int:scan_id>/status", methods=["PATCH"])
@login_required
def update_scan_status(scan_id):
    if not supabase:
        return jsonify({"error": "Supabase not configured."}), 500
    user_id = session.get("user_id")
    data = request.get_json(silent=True) or request.form or {}
    status = data.get("status")
    notes = data.get("notes")

    if not status or status not in {"untreated", "treating", "recovered"}:
        return jsonify({"error": "Invalid status. Must be 'untreated', 'treating', or 'recovered'."}), 400

    update_payload = {"status": status}
    if notes is not None:
        update_payload["notes"] = str(notes).strip()
    if status == "treating":
        update_payload["treated_at"] = datetime.now(timezone.utc).isoformat()

    try:
        response = (
            supabase.table("scans")
            .update(update_payload)
            .eq("id", scan_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data or len(response.data) == 0:
            return jsonify({"error": "Scan not found or unauthorized."}), 404
        return jsonify({"success": True, "data": response.data[0]})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Failed to update scan status: " + str(e)}), 500


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
        raw_conf = data.get("confidence")
        try:
            confidence = int(raw_conf) if raw_conf is not None else None
        except (TypeError, ValueError):
            confidence = None

        raw_follow_up = data.get("follow_up_of")
        try:
            follow_up_of = int(raw_follow_up) if raw_follow_up is not None and str(raw_follow_up).strip() not in ("", "null", "None") else None
        except (TypeError, ValueError):
            follow_up_of = None

        def parse_json_list(val):
            if isinstance(val, list):
                return val
            if isinstance(val, str) and val.strip():
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
                return [val.strip()]
            return []

        organic_options = parse_json_list(data.get("organic_options"))
        chemical_options = parse_json_list(data.get("chemical_options"))
        prevention_tips = parse_json_list(data.get("prevention_tips"))
        safety_note = str(data.get("safety_note") or "").strip()

        insert_data = {
            "user_id": session.get("user_id"),
            "crop_name": data.get("crop_name"),
            "disease_name": data.get("disease_name"),
            "severity": data.get("severity"),
            "cause": data.get("cause", "N/A"),
            "treatment": data.get("treatment"),
            "image_url": data.get("image_url", ""),
            "language": data.get("language", "en"),
            "disease_name_en": data.get("disease_name_en") or data.get("disease_name"),
            "confidence": confidence,
            "organic_options": organic_options,
            "chemical_options": chemical_options,
            "prevention_tips": prevention_tips,
            "safety_note": safety_note,
            "follow_up_of": follow_up_of
        }
        try:
            response = supabase.table("scans").insert(insert_data).execute()
        except Exception as insert_err:
            err_lower = str(insert_err).lower()
            if any(col in err_lower for col in ["follow_up_of", "organic_options", "chemical_options", "prevention_tips", "safety_note"]):
                legacy_data = {
                    k: v for k, v in insert_data.items()
                    if k not in ["follow_up_of", "organic_options", "chemical_options", "prevention_tips", "safety_note"]
                }
                response = supabase.table("scans").insert(legacy_data).execute()
            else:
                raise insert_err

        return jsonify({"success": True, "data": response.data[0] if response.data else insert_data})
    except Exception as e:
        return jsonify({"error": "Failed to save scan: " + str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Image is larger than 5 MB. Please choose a smaller photo."}), 413


if __name__ == "__main__":
    app.run(debug=False, port=int(os.getenv("PORT", 5000)))

# Required by Vercel / Gunicorn WSGI
application = app
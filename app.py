import os
import uuid
import base64
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())

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

# Helpers
def upload_image_to_supabase(image_bytes, filename, mime_type):
    """
    Attempts to upload the scan image to Supabase Storage bucket 'crop-images'.
    Returns the public URL if successful, otherwise None.
    """
    if not supabase:
        return None
    try:
        # Create bucket if it doesn't exist (fails gracefully if it already exists or if we lack permissions)
        try:
            supabase.storage.create_bucket("crop-images", options={"public": True})
        except Exception:
            pass

        # Upload the file
        bucket = supabase.storage.from_("crop-images")
        bucket.upload(
            path=filename,
            file=image_bytes,
            file_options={"content-type": mime_type}
        )
        
        # Get public URL
        public_url = bucket.get_public_url(filename)
        return public_url
    except Exception as e:
        print(f"Failed to upload image to Supabase Storage: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided in request."}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No image selected for uploading."}), 400

    try:
        # Read image data
        image_bytes = image_file.read()
        mime_type = image_file.content_type or 'image/jpeg'
        
        # Check Gemini Key
        if not GEMINI_API_KEY:
            return jsonify({"error": "Gemini API is not configured on the server."}), 500

        # Formulate instructions for JSON generation
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

        # Generate content using typed Parts to avoid validation errors
        response = client.models.generate_content(
            model="gemini-3.6-flash",
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
        # Get raw text and strip markdown code fences if present
        result_text = response.text
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```"):
            # Remove opening fence (e.g. ```json or ```)
            cleaned_text = cleaned_text.split("\n", 1)[-1]
            # Remove closing fence
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text.rsplit("```", 1)[0].strip()

        try:
            analysis_result = json.loads(cleaned_text)
        except json.JSONDecodeError as json_err:
            print(f"JSON parse error: {json_err}")
            print(f"Raw Gemini response:\n{result_text}")
            return jsonify({"error": f"Failed to parse Gemini response as JSON: {str(json_err)}"}), 500

        # Generate unique filename for storage
        file_ext = image_file.filename.split('.')[-1] if '.' in image_file.filename else 'jpg'
        unique_filename = f"scan_{uuid.uuid4().hex}.{file_ext}"

        # Upload image to Supabase Storage or fall back to Base64 data URL
        image_url = upload_image_to_supabase(image_bytes, unique_filename, mime_type)
        if not image_url:
            # Fallback: Base64 data URL
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:{mime_type};base64,{encoded_image}"

        # Include image_url in response so frontend can easily pass it to /save
        analysis_result["image_url"] = image_url

        return jsonify(analysis_result)

    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
def history():
    if not supabase:
        return jsonify({"error": "Supabase connection is not configured."}), 500

    try:
        # Fetch scan results from the database ordered by creation date
        response = supabase.table("scans").select("*").order("created_at", desc=True).execute()
        # In supabase-py v2, response.data holds the actual rows
        return jsonify(response.data)
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500

@app.route('/save', methods=['POST'])
def save():
    if not supabase:
        return jsonify({"error": "Supabase connection is not configured."}), 500

    data = request.json or request.form
    if not data:
        return jsonify({"error": "No scan data provided."}), 400

    # Ensure required fields exist
    required_fields = ["crop_name", "disease_name", "severity", "treatment"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Insert scan record into Supabase scans table
        insert_data = {
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
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))


# 🌿 CropSense.AI

CropSense.AI is an AI-powered agricultural diagnosis and crop health monitoring web application that empowers farmers and growers to instantly identify plant leaf diseases, evaluate severity, and receive actionable, weather-aware treatment guidance by simply uploading a photo of an affected leaf. Leveraging multimodal vision intelligence through OpenRouter alongside free Open-Meteo hyperlocal forecasts, CropSense.AI delivers tailored organic and chemical remediation plans, audible speech read-outs in 8 Indian languages, comprehensive recovery tracking, and downloadable PDF field reports to protect crop yields and promote sustainable farming.

[![Live Demo](https://img.shields.io/badge/Demo-cropsense--ai--theta.vercel.app-1b5e20?style=for-the-badge&logo=vercel)](https://cropsense-ai-theta.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ecf8e?style=for-the-badge&logo=supabase)](https://supabase.com/)

---

## 🚀 Live Demo
Visit the production deployment on Vercel:  
👉 **[https://cropsense-ai-theta.vercel.app](https://cropsense-ai-theta.vercel.app)**

---

## ✨ Features

- **🌐 Multilingual Results & Dynamic Translation:**
  - Full support for 8 languages: English (`en`), Hindi (`hi`), Kannada (`kn`), Tamil (`ta`), Telugu (`te`), Marathi (`mr`), Bengali (`bn`), and Malayalam (`ml`).
  - Dropdown on the analysis page and live report page calling `POST /translate` for seamless on-the-fly report translations, backed by a client-side dictionary (`static/i18n.js`).
- **🎯 Confidence Score & Retake Guidance:**
  - AI confidence percentage bar with color-coded risk grading (green $\ge 80\%$, amber $60-79\%$, red $< 60\%$).
  - Evaluates leaf photo clarity (`good`, `blurry`, `too_dark`, `not_a_leaf`, `multiple_leaves`) and displays helpful retake guidance if confidence is low or image quality is substandard.
- **🌱 Organic & Chemical Treatment Options:**
  - Separate tabbed recommendations for organic treatments (e.g. bio-fungicides, neem sprays) and chemical active ingredients (no commercial brand bias).
  - Practical prevention tips and visible safety precautions (protective equipment, Krishi Vigyan Kendra guidance).
  - Clear "No treatment needed" status for healthy foliage.
- **📊 Interactive Dashboard & Analytics:**
  - Client-side Chart.js charts: Top 5 Diagnosed Diseases (bar chart), Scans per Week trends (line chart), Severity Breakdown (doughnut chart), and Scans per Crop (bar chart).
  - Real-time filtering by crop type and date range (Last 7 Days, Last 30 Days, All Time) syncing charts, summary cards, and history table together.
- **📄 Downloadable PDF Field Reports:**
  - Client-side print stylesheet (`@media print`) enabling one-click "Download PDF" using native browser print-to-PDF.
  - Formatted for clean single-page printing with full support for Indian language typography and no external server-side binary overhead.
- **🔄 Treatment Tracker & Re-Scan Comparison:**
  - Track recovery stages (`untreated`, `treating`, `recovered`), log field notes, and capture treatment timestamps.
  - Link follow-up re-scans with visual progression outcomes (e.g. "Severe $\rightarrow$ Mild (improved)" or "worse").
- **🌦️ Hyperlocal Weather-Aware Advice:**
  - Integrates with Open-Meteo (free, no API key required) via geolocation or city name fallback.
  - Rule-based agronomic alerts analyzing temperature, relative humidity, wind speed, and 48-hour rainfall forecast to warn against pesticide drift, chemical wash-off, and fungal outbreak risks.
- **🔊 Read-Aloud Narration (Web Speech API):**
  - Built-in browser `speechSynthesis` reader with Listen, Pause, Resume, and Stop controls.
  - Sentence-sized chunk queue preventing browser speech truncation bugs.
  - Maps languages to Indian locales (`en-IN`, `hi-IN`, `kn-IN`, `ta-IN`, `te-IN`, `mr-IN`, `bn-IN`, `ml-IN`) with automatic fallback to English when a local voice is not installed on the user's device.
  - Automatic cancellation on page leave or language change.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Backend** | Python 3, Flask, Gunicorn | Lightweight web framework and WSGI server |
| **Vision AI** | OpenRouter API (`OPENROUTER_MODEL`) | Multimodal vision models (e.g., Google Gemini 2.0 Flash) |
| **Database & Auth** | Supabase | PostgreSQL database with Row Level Security (RLS) & Auth |
| **Deployment** | Vercel | Serverless hosting using `@vercel/python` |
| **Data Visualization** | Chart.js 4.4.1 | Client-side responsive charts via jsDelivr CDN |
| **Weather API** | Open-Meteo | Free weather forecast & geocoding endpoints (no API key) |
| **Speech Engine** | Web Speech API | Client-side speech synthesis and audio narration |

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Description | Example / Default |
|---|---|---|
| `SECRET_KEY` | Flask session secret key for cookie signing | `your-secure-random-secret-key` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xyzcompany.supabase.co` |
| `SUPABASE_KEY` | Supabase public `anon` API key | `eyJhbGciOi...` |
| `OPENROUTER_API_KEY` | OpenRouter API key for multimodal model access | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | OpenRouter vision model identifier | `google/gemini-2.0-flash-001` |
| `PORT` *(Optional)* | Local port to run the development server | `5000` |

---

## 💻 Local Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mohitraj072/cropsense-ai.git
   cd cropsense-ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows (Command Prompt / PowerShell):
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key_here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=google/gemini-2.0-flash-001
   ```

5. **Run the database migrations:**
   Execute the SQL statements from [`schema.sql`](schema.sql) in your **Supabase SQL Editor** (see order below).

6. **Start the local development server:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🗄️ SQL Migrations (in `schema.sql` order)

Run these SQL statements in order in the **Supabase SQL Editor** before running or deploying the application:

```sql
-- 1. Create base scans table for persistent scan records
create table public.scans (
  id bigint generated by default as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  crop_name text not null,
  disease_name text not null,
  severity text not null,
  cause text not null default 'N/A',
  treatment text not null,
  image_url text not null default '',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Enable Row Level Security (RLS)
alter table public.scans enable row level security;

-- 3. RLS Policies for authenticated users and anon backend role
create policy "Users can insert own scans" on public.scans
  for insert with check (auth.uid() = user_id);

create policy "Users can view own scans" on public.scans
  for select using (auth.uid() = user_id);

create policy "Allow anon inserts" on public.scans
  for insert to anon with check (true);

create policy "Allow anon reads" on public.scans
  for select to anon using (true);

-- 4. Multilingual support: language code and English disease name
alter table public.scans add column if not exists language text default 'en';
alter table public.scans add column if not exists disease_name_en text;

-- 5. Confidence score
alter table public.scans add column if not exists confidence integer;

-- 6. Organic/chemical treatment options, prevention tips, and safety note
alter table public.scans add column if not exists organic_options jsonb default '[]'::jsonb;
alter table public.scans add column if not exists chemical_options jsonb default '[]'::jsonb;
alter table public.scans add column if not exists prevention_tips jsonb default '[]'::jsonb;
alter table public.scans add column if not exists safety_note text;

-- 7. Treatment tracker with re-scan comparison & update policy
alter table public.scans add column if not exists status text not null default 'untreated';
alter table public.scans add column if not exists treated_at timestamptz;
alter table public.scans add column if not exists notes text;
alter table public.scans add column if not exists follow_up_of bigint references public.scans(id) on delete set null;
create policy "Allow anon updates" on public.scans for update to anon using (true) with check (true);

-- 8. Weather-aware advice persistence
alter table public.scans add column if not exists weather_advice text;
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

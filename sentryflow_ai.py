"""
SentryFlow AI — Enugu State Crime Intelligence Platform
Mobile-optimised | Google Gemini 2.0 Flash | All 17 LGAs

Requirements:
    pip install streamlit pandas google-generativeai folium pillow

Run on laptop:
    python -m streamlit run sentryflow_ai.py

"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import re
import random
import datetime
import io
import base64
import os
import pathlib
import google.generativeai as genai
from dotenv import load_dotenv
import folium
from folium.plugins import HeatMap

# ─────────────────────────────────────────────
# PAGE CONFIG — must be VERY FIRST Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SentryFlow AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# API KEY — secure multi-fallback loading
# ─────────────────────────────────────────────
def _load_api_key() -> str:
    """
    Load Gemini API key with 4 fallback methods in order:
    1. Streamlit Cloud secrets (st.secrets) — for hosted deployment
    2. .env file next to this script — for local use
    3. .env file in current working directory
    4. System environment variables GEMINI_API_KEY or GOOGLE_API_KEY
    """
    # Method 1: Streamlit Cloud secrets
    try:
        key = st.secrets.get("GEMINI_API_KEY", "").strip()
        if key:
            return key
    except Exception:
        pass

    # Method 2: .env file next to this script
    _script_env = pathlib.Path(__file__).parent / ".env"
    if _script_env.exists():
        load_dotenv(dotenv_path=_script_env, override=True)

    # Method 3: .env in current working directory
    _cwd_env = pathlib.Path(os.getcwd()) / ".env"
    if _cwd_env.exists():
        load_dotenv(dotenv_path=_cwd_env, override=True)

    # Method 4: System environment variables
    key = (
        os.getenv("GEMINI_API_KEY", "").strip() or
        os.getenv("GOOGLE_API_KEY", "").strip()
    )
    return key

GEMINI_API_KEY = _load_api_key()

# ─────────────────────────────────────────────
# ENUGU STATE — ALL 17 LGAs
# ─────────────────────────────────────────────
ENUGU_CENTER = (6.5244, 7.5086)

LGA_BOUNDS = {
    "Enugu North":    {"lat_range": (6.455, 6.510), "lng_range": (7.490, 7.545)},
    "Enugu South":    {"lat_range": (6.405, 6.458), "lng_range": (7.488, 7.548)},
    "Enugu East":     {"lat_range": (6.408, 6.465), "lng_range": (7.500, 7.575)},
    "Agwu":           {"lat_range": (6.000, 6.180), "lng_range": (7.600, 7.800)},
    "Aninri":         {"lat_range": (6.050, 6.220), "lng_range": (7.380, 7.560)},
    "Awgu":           {"lat_range": (6.050, 6.230), "lng_range": (7.450, 7.650)},
    "Ezeagu":         {"lat_range": (6.250, 6.430), "lng_range": (7.350, 7.530)},
    "Igbo-Eze North": {"lat_range": (6.680, 6.870), "lng_range": (7.430, 7.630)},
    "Igbo-Eze South": {"lat_range": (6.560, 6.700), "lng_range": (7.420, 7.600)},
    "Isi-Uzo":        {"lat_range": (6.530, 6.730), "lng_range": (7.600, 7.800)},
    "Igbo-Etiti":     {"lat_range": (6.430, 6.560), "lng_range": (7.200, 7.400)},
    "Nkanu East":     {"lat_range": (6.250, 6.430), "lng_range": (7.550, 7.730)},
    "Nkanu West":     {"lat_range": (6.280, 6.450), "lng_range": (7.430, 7.580)},
    "Nsukka":         {"lat_range": (6.820, 7.000), "lng_range": (7.350, 7.530)},
    "Oji-River":      {"lat_range": (6.620, 6.790), "lng_range": (7.280, 7.460)},
    "Udenu":          {"lat_range": (6.880, 7.060), "lng_range": (7.430, 7.620)},
    "Udi":            {"lat_range": (6.280, 6.460), "lng_range": (7.270, 7.450)},
    "Uzo-Uwani":      {"lat_range": (6.700, 6.880), "lng_range": (7.130, 7.320)},
}

LANDMARKS = {
    "Agric Bank Junction":          (6.4668, 7.5068, "Enugu North"),
    "Presidential Road":            (6.4720, 7.5055, "Enugu North"),
    "Ogui Road":                    (6.4780, 7.5120, "Enugu North"),
    "Okpara Avenue":                (6.4695, 7.5042, "Enugu North"),
    "Independence Layout":          (6.4658, 7.4985, "Enugu North"),
    "Trans-Ekulu":                  (6.4820, 7.5340, "Enugu North"),
    "Emene Industrial Layout":      (6.4960, 7.5620, "Enugu North"),
    "Asata":                        (6.4720, 7.5015, "Enugu North"),
    "Abakpa Nike":                  (6.4850, 7.5430, "Enugu North"),
    "Nike Lake Road":               (6.4910, 7.5480, "Enugu North"),
    "Thinkers Corner":              (6.4760, 7.5280, "Enugu North"),
    "Abakiliki Road Junction":      (6.4900, 7.5200, "Enugu North"),
    "Shoprite Enugu":               (6.4432, 7.5268, "Enugu South"),
    "Coal Camp":                    (6.4395, 7.4960, "Enugu South"),
    "New Haven":                    (6.4475, 7.5195, "Enugu South"),
    "Uwani":                        (6.4355, 7.5048, "Enugu South"),
    "GRA Enugu":                    (6.4415, 7.5125, "Enugu South"),
    "Obiagu Road":                  (6.4318, 7.5005, "Enugu South"),
    "Achara Layout":                (6.4215, 7.5360, "Enugu South"),
    "Zik Avenue":                   (6.4440, 7.5085, "Enugu South"),
    "Gariki":                       (6.4280, 7.5150, "Enugu South"),
    "Idaw River Junction":          (6.4190, 7.5080, "Enugu South"),
    "Holy Ghost Cathedral":         (6.4515, 7.5092, "Enugu East"),
    "Otigba Street":                (6.4565, 7.5215, "Enugu East"),
    "Maryland":                     (6.4380, 7.5350, "Enugu East"),
    "Sapper":                       (6.4450, 7.5420, "Enugu East"),
    "Ninth Mile Corner":            (6.4120, 7.5510, "Enugu East"),
    "Kenyatta Street":              (6.4335, 7.5180, "Enugu East"),
    "Nsukka Town Centre":           (6.8567, 7.3958, "Nsukka"),
    "University of Nigeria Nsukka": (6.8698, 7.4103, "Nsukka"),
    "Ogurute Market Nsukka":        (6.8540, 7.3880, "Nsukka"),
    "Nsukka Motor Park":            (6.8600, 7.3920, "Nsukka"),
    "Obollo-Afor":                  (6.8210, 7.5520, "Igbo-Eze North"),
    "Obollo-Eke Market":            (6.8150, 7.5480, "Igbo-Eze North"),
    "Iheakpu-Awka":                 (6.7650, 7.5020, "Igbo-Eze North"),
    "Aji":                          (6.6250, 7.4920, "Igbo-Eze South"),
    "Ibagwa-Ani":                   (6.6480, 7.5380, "Igbo-Eze South"),
    "Ikem":                         (6.5820, 7.6950, "Isi-Uzo"),
    "Isu":                          (6.6120, 7.7100, "Isi-Uzo"),
    "Eha-Amufu":                    (6.6550, 7.7320, "Isi-Uzo"),
    "Obollo-Etiti":                 (6.9200, 7.5250, "Udenu"),
    "Enugu-Ezike":                  (6.9520, 7.4850, "Udenu"),
    "Oji-River Town":               (6.6840, 7.3620, "Oji-River"),
    "Inyi":                         (6.7100, 7.3850, "Oji-River"),
    "Adani":                        (6.7620, 7.1980, "Uzo-Uwani"),
    "Nimbo":                        (6.7850, 7.2350, "Uzo-Uwani"),
    "Nkanu East Headquarters":      (6.3350, 7.6550, "Nkanu East"),
    "Nomeh":                        (6.3620, 7.6820, "Nkanu East"),
    "Agbani":                       (6.3280, 7.5420, "Nkanu West"),
    "Nkanu West Secretariat":       (6.3500, 7.5150, "Nkanu West"),
    "Agbogugu":                     (6.3020, 7.4180, "Ezeagu"),
    "Aguobu-Owa":                   (6.3350, 7.3920, "Ezeagu"),
    "Mmaku":                        (6.3650, 7.4650, "Ezeagu"),
    "Awgu Town":                    (6.0680, 7.5580, "Awgu"),
    "Nomeh Awgu":                   (6.1020, 7.5420, "Awgu"),
    "Agwu Town":                    (6.0420, 7.7120, "Agwu"),
    "Okpanku":                      (6.0850, 7.7450, "Agwu"),
    "Aninri Town":                  (6.1480, 7.4680, "Aninri"),
    "Oduma":                        (6.0950, 7.4420, "Aninri"),
    "Udi Town":                     (6.3180, 7.3580, "Udi"),
    "Obinagu":                      (6.3650, 7.3850, "Udi"),
    "Oguta Road Udi":               (6.3420, 7.3280, "Udi"),
    "Ogurute":                      (6.4980, 7.3150, "Igbo-Etiti"),
    "Ozalla":                       (6.5120, 7.2880, "Igbo-Etiti"),
    "Umulokpa":                     (6.5350, 7.3420, "Igbo-Etiti"),
}

CATEGORIES = [
    "Theft / Robbery", "Kidnapping", "Vandalism", "Harassment / Assault",
    "Fraud / Scam", "Traffic Incident", "Suspicious Activity",
    "Drug-Related", "Domestic Violence", "Other",
]

URGENCY_LABELS = {
    1: ("LOW",      "#4ade80"),
    2: ("MODERATE", "#facc15"),
    3: ("HIGH",     "#fb923c"),
    4: ("CRITICAL", "#f87171"),
    5: ("EXTREME",  "#dc2626"),
}

COLS = ["id", "timestamp", "category", "location", "lga", "urgency", "lat", "lng", "summary", "image_path"]

# ─────────────────────────────────────────────
# PERSISTENT STORAGE — saved on the host laptop
# All reports from all devices are written here
# ─────────────────────────────────────────────
# Stored in same folder as this script
DB_PATH    = pathlib.Path(__file__).parent / "sentryflow_incidents.csv"
IMAGES_DIR = pathlib.Path(__file__).parent / "sentryflow_evidence"
IMAGES_DIR.mkdir(exist_ok=True)   # Create folder on first run

def load_incidents() -> pd.DataFrame:
    """Load all saved incidents from disk. Returns empty DataFrame if none yet."""
    if DB_PATH.exists():
        try:
            df = pd.read_csv(DB_PATH, dtype=str)
            # Restore correct types
            df["urgency"] = pd.to_numeric(df["urgency"], errors="coerce").fillna(3).astype(int)
            df["lat"]     = pd.to_numeric(df["lat"],     errors="coerce")
            df["lng"]     = pd.to_numeric(df["lng"],     errors="coerce")
            # Ensure all expected columns exist
            for col in COLS:
                if col not in df.columns:
                    df[col] = ""
            df["image_path"] = df["image_path"].fillna("")
            return df[COLS].reset_index(drop=True)
        except Exception:
            return pd.DataFrame(columns=COLS)
    return pd.DataFrame(columns=COLS)

def save_incident(row: dict):
    """Append a single new incident row to the CSV on disk."""
    new_row = pd.DataFrame([row], columns=COLS)
    if DB_PATH.exists():
        new_row.to_csv(DB_PATH, mode="a", header=False, index=False)
    else:
        new_row.to_csv(DB_PATH, mode="w", header=True, index=False)

def save_evidence_image(incident_id: str, img_bytes: bytes, filename: str) -> str:
    """
    Save evidence photo to the sentryflow_evidence folder.
    Returns the relative file path, or empty string if no image.
    """
    if not img_bytes:
        return ""
    try:
        ext = pathlib.Path(filename).suffix.lower() or ".jpg"
        safe_ext = ext if ext in [".jpg",".jpeg",".png",".webp"] else ".jpg"
        img_filename = f"{incident_id}{safe_ext}"
        img_path     = IMAGES_DIR / img_filename
        img_path.write_bytes(img_bytes)
        return str(img_path)
    except Exception:
        return ""

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');
:root {
    --bg:#0a0e1a; --surface:#111827; --surface2:#0d1b2a;
    --border:#1e3a5f; --accent:#00d4ff; --accent2:#ff4d6d;
    --text:#e2e8f0; --muted:#64748b;
    --font-hd:'Rajdhani',sans-serif;
    --font-mono:'Share Tech Mono',monospace;
    --font-body:'Inter',sans-serif;
}
html,body,.stApp { background-color:var(--bg)!important; color:var(--text)!important; font-family:var(--font-body); }
#MainMenu,footer,header { visibility:hidden; }
section[data-testid="stSidebar"] { background:var(--surface)!important; border-right:1px solid var(--border)!important; }
section[data-testid="stSidebar"] * { color:var(--text)!important; }
textarea,input,select,.stTextInput>div>div>input {
    background:var(--surface2)!important; color:var(--text)!important;
    border:1px solid var(--border)!important; border-radius:10px!important;
    font-family:var(--font-body)!important; font-size:1rem!important;
    padding:0.6rem 0.9rem!important;
}
textarea { min-height:140px!important; line-height:1.6!important; }
.stSelectbox>div>div { background:var(--surface2)!important; border:1px solid var(--border)!important; border-radius:10px!important; }
.stButton>button {
    background:linear-gradient(135deg,#005f8e,#00d4ff)!important;
    color:#0a0e1a!important; font-family:var(--font-hd)!important;
    font-size:1.2rem!important; font-weight:700!important;
    border:none!important; border-radius:12px!important;
    min-height:56px!important; width:100%!important;
    padding:0.8rem 1.5rem!important; touch-action:manipulation!important;
}
.stButton>button:hover { opacity:.88; }
.stButton>button:active { transform:scale(.97); }
.stSelectbox label,.stSlider label,.stTextArea label,.stFileUploader label,p,li { color:var(--text)!important; font-size:0.95rem!important; }
[data-testid="stMetric"] { background:var(--surface)!important; border:1px solid var(--border)!important; border-radius:12px!important; padding:.9rem 1rem!important; }
[data-testid="stMetricLabel"] { color:var(--muted)!important; font-size:.8rem!important; }
[data-testid="stMetricValue"] { color:var(--accent)!important; font-family:var(--font-hd)!important; font-size:1.8rem!important; }
.stDataFrame { background:var(--surface)!important; border-radius:10px!important; }
.stDataFrame th { background:var(--surface2)!important; color:var(--accent)!important; }
.stDataFrame td { color:var(--text)!important; }
hr { border-color:var(--border)!important; }
[data-testid="stFileUploader"] { background:var(--surface2)!important; border:1px dashed var(--border)!important; border-radius:10px!important; padding:1rem!important; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface)!important; border-radius:12px!important; padding:4px!important; gap:4px!important; border:1px solid var(--border)!important; }
.stTabs [data-baseweb="tab"] { background:transparent!important; color:var(--muted)!important; font-family:var(--font-hd)!important; font-size:1.05rem!important; font-weight:600!important; border-radius:8px!important; min-height:44px!important; padding:0.5rem 1rem!important; border:none!important; flex:1!important; }
.stTabs [aria-selected="true"] { background:var(--surface2)!important; color:var(--accent)!important; border-bottom:2px solid var(--accent)!important; }
.stTabs [data-baseweb="tab-panel"] { padding-top:1rem!important; }
@media (max-width:768px) { .block-container { padding:0.5rem 0.75rem 3rem!important; } [data-testid="stMetricValue"] { font-size:1.4rem!important; } }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#050d1a 0%,#0a1f3a 50%,#050d1a 100%);
            border:1px solid #1e3a5f;border-radius:14px;
            padding:1.1rem 1.4rem;margin-bottom:1rem;position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(
    0deg,transparent,transparent 28px,rgba(0,212,255,.04) 28px,rgba(0,212,255,.04) 29px);"></div>
  <div style="position:relative;z-index:1;display:flex;align-items:center;
              justify-content:space-between;flex-wrap:wrap;gap:.5rem;">
    <div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:clamp(1.4rem,5vw,2.2rem);
                  font-weight:700;color:#00d4ff;letter-spacing:.1em;line-height:1;">
        🛡️ SENTRYFLOW <span style="color:#ff4d6d;">AI</span>
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:.72rem;
                  color:#64748b;letter-spacing:.12em;margin-top:.25rem;">
        ENUGU STATE CRIME INTELLIGENCE PLATFORM
      </div>
    </div>
    <div style="display:flex;gap:.4rem;flex-wrap:wrap;">
      <span style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:6px;
                   padding:.3rem .7rem;font-family:'Share Tech Mono',monospace;
                   font-size:.65rem;color:#4ade80;">🔒 SECURE</span>
      <span style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:6px;
                   padding:.3rem .7rem;font-family:'Share Tech Mono',monospace;
                   font-size:.65rem;color:#00d4ff;">👁 ANONYMOUS</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "incidents" not in st.session_state:
    # Load all previously saved incidents from disk on every fresh start
    st.session_state.incidents = load_incidents()

# ── Show clear API key status banner ─────────────────────────────────────────
if not GEMINI_API_KEY:
    st.error(
        "**API key not found.** The app cannot classify reports without it.\n\n"
        "**Fix:** Open the `.env` file in your project folder and make sure it contains:\n\n"
        "`GEMINI_API_KEY=AIzaSyYourKeyHere`\n\n"
        "Save the file and restart the app with START_SENTRYFLOW.bat"
    )
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def scrub_pii(text: str) -> str:
    text = re.sub(r"\b(\+?234|0)[789]\d{9}\b", "[PHONE REDACTED]", text)
    text = re.sub(r"\b(Mr|Mrs|Miss|Dr|Chief|Barr)\.?\s+[A-Z][a-z]+\b", "[NAME REDACTED]", text)
    return text

def resolve_coords(location_str: str, lga: str) -> tuple:
    loc_lower = location_str.lower()
    for name, data in LANDMARKS.items():
        if name.lower() in loc_lower:
            lat, lng, _ = data
            j = lambda: random.uniform(-0.002, 0.002)
            return (round(lat + j(), 5), round(lng + j(), 5))
    lga_pts = [(d[0], d[1]) for d in LANDMARKS.values() if d[2] == lga]
    if lga_pts:
        lat, lng = random.choice(lga_pts)
        j = lambda: random.uniform(-0.003, 0.003)
        return (round(lat + j(), 5), round(lng + j(), 5))
    b = LGA_BOUNDS.get(lga, {"lat_range": (6.44, 6.47), "lng_range": (7.50, 7.52)})
    return (round(random.uniform(*b["lat_range"]), 5),
            round(random.uniform(*b["lng_range"]), 5))

def call_gemini(text: str, image_bytes=None) -> dict:
    genai.configure(api_key=GEMINI_API_KEY.strip())
    model    = genai.GenerativeModel("gemini-2.5-flash")
    ALL_LGAS = list(LGA_BOUNDS.keys())
    prompt   = f"""You are an AI crime-report analyst for Enugu State, Nigeria.
Analyse the report below and return ONLY a valid JSON object with these exact keys:
- "category": one of {CATEGORIES}
- "location": specific street, junction, landmark or town in Enugu State
- "lga": one of {ALL_LGAS} — match the location to the correct LGA
- "urgency": integer 1 to 5 (1=low, 5=life-threatening emergency)
- "summary": one sentence anonymised summary, remove all names and phone numbers

Return ONLY the raw JSON object. No markdown, no code fences, no explanation.

Report:
\"\"\"{text}\"\"\"
"""
    contents = [prompt]
    if image_bytes:
        import PIL.Image
        contents = [prompt, PIL.Image.open(io.BytesIO(image_bytes))]
    resp = model.generate_content(contents)
    raw  = resp.text.strip()
    raw  = re.sub(r"^```(?:json)?", "", raw).strip()
    raw  = re.sub(r"```$", "", raw).strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group(0)
    data = json.loads(raw)
    if data.get("category") not in set(CATEGORIES):
        data["category"] = "Other"
    if data.get("lga") not in set(LGA_BOUNDS):
        data["lga"] = "Enugu North"
    data.setdefault("location", "Unknown Location")
    data.setdefault("urgency", 3)
    data["summary"] = scrub_pii(data.get("summary", text[:120]))
    data["urgency"]  = max(1, min(5, int(data["urgency"])))
    return data

def add_incident(parsed: dict, img_bytes: bytes = None, img_filename: str = "") -> tuple:
    """Save incident to CSV and optionally archive the evidence photo."""
    total_saved = len(load_incidents())
    new_id   = f"SF-{1000 + total_saved}"
    lat, lng = resolve_coords(parsed["location"], parsed["lga"])
    # Save evidence image first so path is available for the CSV row
    image_path = save_evidence_image(new_id, img_bytes, img_filename) if img_bytes else ""
    row = {
        "id":         new_id,
        "timestamp":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category":   parsed["category"],
        "location":   parsed["location"],
        "lga":        parsed["lga"],
        "urgency":    parsed["urgency"],
        "lat":        lat,
        "lng":        lng,
        "summary":    parsed["summary"],
        "image_path": image_path,
    }
    save_incident(row)
    st.session_state.incidents = load_incidents()
    return new_id, lat, lng

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;font-weight:700;
                color:#00d4ff;letter-spacing:.1em;margin-bottom:1rem;">
        🔍 FILTERS &amp; STATS
    </div>""", unsafe_allow_html=True)

    df_all = st.session_state.incidents
    lga_options = ["All LGAs"] + sorted(df_all["lga"].unique().tolist()) if not df_all.empty else ["All LGAs"]
    cat_options = ["All Categories"] + sorted(df_all["category"].unique().tolist()) if not df_all.empty else ["All Categories"]

    sel_lga = st.selectbox("Filter by LGA",      lga_options)
    sel_urg = st.slider("Min Urgency", 1, 5, 1)
    sel_cat = st.selectbox("Filter by Category", cat_options)

    st.markdown("---")
    st.metric("Total Incidents", len(df_all))
    st.metric("Critical (≥4)",   int((df_all["urgency"] >= 4).sum()) if not df_all.empty else 0)
    st.metric("Active LGAs",     df_all["lga"].nunique() if not df_all.empty else 0)
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;font-size:.68rem;
                color:#475569;line-height:1.9;">
    🔒 ALL REPORTS ANONYMISED<br>
    📡 AI: GEMINI 2.5 FLASH<br>
    🗺️ ALL 17 LGAs COVERED<br>
    ✅ REAL REPORTS ONLY
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
df_view = st.session_state.incidents.copy()
if not df_view.empty:
    if sel_lga != "All LGAs":
        df_view = df_view[df_view["lga"] == sel_lga]
    if sel_urg > 1:
        df_view = df_view[df_view["urgency"] >= sel_urg]
    if sel_cat != "All Categories":
        df_view = df_view[df_view["category"] == sel_cat]

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_report, tab_map, tab_feed = st.tabs([
    "📢  Report Incident",
    "🗺️  Live Map",
    "📋  Incident Feed",
])

# ══════════════════════════════════════════════
# TAB 1 — REPORT FORM
# ══════════════════════════════════════════════
with tab_report:
    st.markdown("""
    <div style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:10px;
                padding:.85rem 1.1rem;margin-bottom:1rem;font-size:.85rem;color:#64748b;">
        ⚡ Your identity is never stored.
        All names and phone numbers are automatically removed before saving.
    </div>""", unsafe_allow_html=True)

    incident_text = st.text_area(
        "📝 Describe the incident in detail",
        placeholder=(
            "Example: Armed robbery near Agric Bank Junction around 9pm. "
            "Three men on a motorcycle, one had a gun, snatched a bag "
            "and rode towards Coal Camp..."
        ),
        height=180,
        key="incident_input",
    )

    manual_lga = st.selectbox(
        "📍 Select LGA where it happened  "
        "(leave on Auto-detect — AI will identify it from your description)",
        ["Auto-detect"] + sorted(LGA_BOUNDS.keys()),
        key="manual_lga",
    )

    uploaded_img = st.file_uploader(
        "📸 Attach evidence photo (optional)",
        type=["jpg", "jpeg", "png", "webp"],
        key="photo_upload",
    )
    if uploaded_img:
        st.image(uploaded_img, caption="Photo attached", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("🛡️  SUBMIT REPORT", type="primary")

    if submit:
        if not incident_text.strip():
            st.warning("⚠️ Please describe the incident before submitting.")
        else:
            with st.spinner("🔍 AI is analysing your report — please wait..."):
                try:
                    img_bytes  = uploaded_img.read() if uploaded_img else None
                    img_fname  = uploaded_img.name if uploaded_img else ""
                    parsed     = call_gemini(incident_text, img_bytes)
                    if manual_lga != "Auto-detect":
                        parsed["lga"] = manual_lga
                    new_id, lat, lng = add_incident(parsed, img_bytes, img_fname)
                    st.session_state.last_result = {
                        **parsed, "id": new_id, "lat": lat, "lng": lng,
                    }
                    st.rerun()
                except json.JSONDecodeError:
                    st.error(
                        "❌ The AI returned an unexpected response. "
                        "Please add more detail to your report and try again."
                    )
                except Exception as e:
                    st.error(f"❌ Submission failed: {e}")

    # Confirmation card
    if st.session_state.last_result:
        r = st.session_state.last_result
        urg_label, urg_color = URGENCY_LABELS.get(r["urgency"], ("UNKNOWN", "#aaa"))
        filled = "█" * r["urgency"]
        empty  = "░" * (5 - r["urgency"])
        st.markdown(f"""
        <div style="background:#0d1b2a;border:1px solid #00d4ff;border-radius:14px;
                    padding:1.3rem;margin-top:1.2rem;">
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;font-weight:700;
                      color:#00d4ff;margin-bottom:.9rem;letter-spacing:.06em;">
            ✅ REPORT {r['id']} SUCCESSFULLY FILED
          </div>
          <table style="width:100%;border-collapse:collapse;font-size:.92rem;color:#e2e8f0;">
            <tr><td style="color:#64748b;padding:.3rem 0;width:100px;">Category</td>
                <td style="font-weight:600;padding

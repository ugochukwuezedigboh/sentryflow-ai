# 🛡️ SentryFlow AI
### Enugu State Crime Intelligence Platform

> Anonymous, AI-powered crime reporting for all 17 LGAs of Enugu State, Nigeria.
> Built for the **3MTT NextGen Knowledge Showcase 2026** — Digital Inclusion pillar.

---

## 🔴 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enugu-crime-report.streamlit.app)

**Live URL:** https://enugu-crime-report.streamlit.app

---

## What It Does

SentryFlow AI is a fully working, anonymous crime intelligence platform that allows any citizen in Enugu State to report a crime from any smartphone or laptop in under 60 seconds. Google Gemini 2.5 Flash AI automatically classifies every report, extracts the location and urgency, and plots it on a live heatmap covering all 17 Local Government Areas. Every report — including any evidence photos attached — is permanently archived.

### Core Features

| Feature | Description |
|---|---|
| **AI Classification** | Gemini 2.5 Flash reads the report and assigns category, LGA, location and urgency (1–5) automatically |
| **Full Anonymity** | All personal names and phone numbers stripped before storage — identity never recorded |
| **Live Heatmap** | Every report plotted instantly on an interactive map of all 17 Enugu State LGAs |
| **Evidence Photo Archive** | Citizens attach photos to reports — saved permanently to `sentryflow_evidence/` folder |
| **Persistent CSV Archive** | Every report saved to `sentryflow_incidents.csv` — never lost on restart or refresh |
| **Evidence Gallery** | All archived photos displayed in a searchable gallery in the Incident Feed tab |
| **10 Crime Categories** | Theft, Kidnapping, Vandalism, Assault, Fraud, Traffic, Suspicious Activity, Drug-Related, Domestic Violence, Other |
| **Mobile-First Design** | Works on any smartphone browser — no app download required |
| **CSV Data Export** | Authorities export filtered incident data for analysis and action |

---

## Evidence Archiving System

When a citizen attaches a photo to their crime report, SentryFlow AI:

1. Saves the image to the `sentryflow_evidence/` folder, named after its unique incident ID — e.g. `SF-1005.jpg`
2. Records the full file path in the `image_path` column of the CSV archive so every report links directly to its photo
3. Displays a **📸 Photo archived** confirmation on the submission card
4. Shows all evidence photos in a 3-column gallery in the **Incident Feed** tab, each labelled with the Incident ID, category and timestamp

The archive structure on the host system:

```
sentryflow-ai/
├── sentryflow_incidents.csv          ← full text archive of all reports
└── sentryflow_evidence/              ← permanent evidence photo archive
    ├── SF-1000.jpg
    ├── SF-1003.png
    └── SF-1007.jpg
```

The archive status bar in the Feed tab shows live counts:

```
💾 12 incidents archived · CSV: sentryflow_incidents.csv · Photos: sentryflow_evidence/ (5 files)
```

---

## Crime Categories

Theft / Robbery · **Kidnapping** · Vandalism · Harassment / Assault · Fraud / Scam ·
Traffic Incident · Suspicious Activity · Drug-Related · Domestic Violence · Other

---

## All 17 LGAs Covered

| City LGAs | Other LGAs |
|---|---|
| Enugu North | Nsukka · Udenu · Igbo-Eze North · Igbo-Eze South |
| Enugu South | Oji-River · Uzo-Uwani · Igbo-Etiti |
| Enugu East | Nkanu East · Nkanu West · Ezeagu |
| | Agwu · Aninri · Awgu · Udi · Isi-Uzo |

---

## Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/ugochukwuezedigboh/sentryflow-ai.git
cd sentryflow-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
copy .env.example .env
```
Open `.env` in Notepad and replace the placeholder with your Gemini API key from [aistudio.google.com](https://aistudio.google.com):
```
GEMINI_API_KEY=AIzaSyYourKeyHere
```

### 4. Run the app
```bash
python -m streamlit run sentryflow_ai.py
```
Open `http://localhost:8501` in your browser.

---

## Project Structure

```
sentryflow-ai/
├── sentryflow_ai.py              # Main application
├── requirements.txt              # Python dependencies
├── .env.example                  # API key template (safe to share)
├── .env                          # Your actual API key (NOT on GitHub)
├── .gitignore                    # Protects .env, CSV and evidence photos
├── START_SENTRYFLOW.bat          # Windows one-click launcher
├── sentryflow_incidents.csv      # Auto-created incident archive (local only)
└── sentryflow_evidence/          # Auto-created evidence photo archive (local only)
```

---

## Deployment on Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** and select this repository
4. Set main file to `sentryflow_ai.py`
5. Under **Advanced settings → Secrets**, add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
6. Click **Deploy**

> **Note:** On Streamlit Cloud the evidence photos and CSV archive are stored in the cloud instance filesystem. For permanent long-term archiving in production, a cloud storage service such as AWS S3 or Google Cloud Storage is recommended.

---

## Tech Stack

| Component | Technology |
|---|---|
| Web framework | Streamlit |
| AI classification | Google Gemini 2.5 Flash |
| Map rendering | Folium + OpenStreetMap |
| CSV archive | Pandas + persistent CSV |
| Evidence archive | Python pathlib + local filesystem |
| API key security | python-dotenv + Streamlit secrets |
| Language | Python 3.9+ |
| Hosting | Streamlit Community Cloud |

---

## Security

- API key stored in `.env` file — never hardcoded in the source code
- `.env`, `sentryflow_incidents.csv` and `sentryflow_evidence/` are all listed in `.gitignore` and will never be uploaded to GitHub
- All submitted names and phone numbers are scrubbed by regex before any data is stored
- Reports are anonymous by design — no login, no identity, no tracking

---

## Declaration of AI Usage

This project was built with the assistance of **Claude AI (Anthropic)** for code generation, debugging, iterative development, UI design, and documentation throughout the entire build process. **Google Gemini 2.5 Flash** is integrated directly into the application to classify submitted crime reports in real time. All final decisions, testing, and deployment were carried out by the developer.

---

## Sustainability Plan

| Phase | Timeline | Action | Cost |
|---|---|---|---|
| Phase 1 | Now | Live on Streamlit Cloud. Shared with CDAs and neighbourhood watch groups | ₦0 |
| Phase 2 | Month 3 | Partner with Enugu State Police Command. Apply for 3MTT scale-up grant | ₦0 |
| Phase 3 | Month 6 | Dedicated server. Add SMS reporting via Twilio for rural LGAs | Low |
| Phase 4 | Year 2 | Formal adoption as official Enugu State digital crime reporting platform | State budget |

---

## About

Built by **Ugochukwu Ezedigboh** as part of the **3MTT Nigeria Fellowship Programme**.
Enugu State · Nigeria · 2026

*Making Enugu State safer — one anonymous report at a time.*

# 🛡️ SentryFlow AI
### Enugu State Crime Intelligence Platform

> Anonymous, AI-powered crime reporting for all 17 LGAs of Enugu State, Nigeria.  
> Built for the **3MTT NextGen Knowledge Showcase 2026** — Digital Inclusion pillar.

---

## What It Does

SentryFlow AI allows any citizen in Enugu State to anonymously report a crime from any smartphone or laptop in under 60 seconds. Google Gemini AI automatically classifies every report, extracts the location and urgency, and plots it on a live heatmap covering all 17 Local Government Areas.

- **Anonymous** — no identity ever stored, names and phone numbers auto-removed
- **AI-powered** — Google Gemini 2.5 Flash classifies every report instantly
- **Mobile-first** — works on any phone browser, no app download needed
- **Persistent archive** — every report saved permanently to CSV on the host system
- **All 17 LGAs** — Enugu North, South, East, Nsukka, Udi, Awgu, Agwu, and 10 more

---

## Crime Categories

Theft / Robbery · Kidnapping · Vandalism · Harassment / Assault · Fraud / Scam ·  
Traffic Incident · Suspicious Activity · Drug-Related · Domestic Violence · Other

---

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sentryflow-ai.streamlit.app)

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
Open `.env` in Notepad and replace the placeholder with your Gemini API key from [aistudio.google.com](https://aistudio.google.com).

```
GEMINI_API_KEY=AIzaSyYourKeyHere
```

### 4. Run the app
```bash
# Laptop only
python -m streamlit run sentryflow_ai.py

# Accessible on mobile (same Wi-Fi)
python -m streamlit run sentryflow_ai.py --server.address 0.0.0.0 --server.port 8502
```

Then open `http://localhost:8502` on your laptop or the Network URL on your phone.

---

## Project Structure

```
sentryflow-ai/
├── sentryflow_ai.py          # Main application
├── requirements.txt          # Python dependencies
├── .env.example              # API key template (safe to share)
├── .env                      # Your actual API key (NOT on GitHub)
├── .gitignore                # Protects .env and incident data
├── START_SENTRYFLOW.bat      # Windows one-click launcher
└── sentryflow_incidents.csv  # Auto-created incident archive (local only)
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

---

## Tech Stack

| Component | Technology |
|---|---|
| Web framework | Streamlit |
| AI classification | Google Gemini 2.5 Flash |
| Map rendering | Folium + OpenStreetMap |
| Data storage | CSV (local persistent archive) |
| Language | Python 3.9+ |

---

## Declaration of AI Usage

This project was built with the assistance of **Claude AI (Anthropic)** for code generation, debugging, and iterative development. **Google Gemini 2.5 Flash** is integrated directly into the application to classify submitted crime reports in real time. All testing, deployment, and final decisions were carried out by the developer.

---

## About

Built by **Ugochukwu Ezedigboh** as part of the **3MTT Nigeria Fellowship Programme**.  
Enugu State · Nigeria · 2026

*Making Enugu State safer — one anonymous report at a time.*

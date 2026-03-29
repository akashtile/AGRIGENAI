<div align="center">

<img src="https://img.shields.io/badge/ET%20HACK%202026-🏆%20Agricultural%20Advisory%20Track-22c55e?style=for-the-badge&labelColor=0d1a0f" />

# 🌾 AgriGenAI — Farming Copilot

**AI-powered agricultural advisory for Indian farmers.**  
Multi-modal · Multi-lingual · Offline-first · 

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-f97316?style=flat-square)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-4ade80?style=flat-square)](LICENSE)

</div>

---

## What is AgriGenAI?

AgriGenAI is a full-stack AI farming assistant built for the **— Agricultural Advisory Agents** track. It gives Indian farmers actionable, personalised guidance through:

- Natural language chat in **Hindi, Marathi, Tamil, English** and other Indian languages
- **Voice input** via Whisper STT — speak your question, get an answer
- **Crop planning** with soil test data (NPK, pH), season, and location
- **Pest & disease detection** from crop photos using vision AI
- **10-day weather forecasts** with farming-specific alerts
- **Market price forecasting** for major crops
- **Government scheme discovery** (PM-KISAN, PMFBY, KCC, and more)
- **Full offline fallback** — works without internet using an ICAR-grounded local knowledge base

---

## Demo

```
Frontend  →  http://localhost:8501
Backend   →  http://localhost:8000
API Docs  →  http://localhost:8000/docs
```

---

## Features

| Feature | Status | Details |
|---|---|---|
| Multi-language Chat | ✅ | Groq LLaMA 3.3 70B, auto-detects and responds in user's language |
| Voice Input (STT) | ✅ | Whisper Large V3 via Groq — all Indian languages |
| Crop Planning | ✅ | Soil type, NPK, pH, season, water availability, previous crop |
| Full-Year Calendar | ✅ | 12-month farming calendar with month-by-month activities |
| Pest & Disease Detection | ✅ | Groq LLaMA 4 Scout Vision — upload any crop photo |
| Market Price Forecast | ✅ | AI price forecast + offline MSP fallback |
| 10-Day Weather | ✅ | Open-Meteo API, sunrise/sunset, UV, rain probability chart |
| Government Schemes | ✅ | RAG over schemes.json + AI explanation |
| Offline Mode | ✅ | 23-topic ICAR knowledge base, zero internet needed |
| Guardrails | ✅ | Topic filtering, chemical dosage validation, input sanitisation |
| Response Caching | ✅ | In-memory cache for market and scheme responses |
| Audit Log | ✅ | Every API call, guardrail trigger, and offline fallback logged |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.111 + Uvicorn 0.29 |
| Frontend UI | Streamlit 1.35 |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Vision Model | Groq — Meta LLaMA 4 Scout 17B |
| Voice / STT | Groq — Whisper Large V3 |
| Weather | Open-Meteo API (free, no key required) |
| Geocoding | Open-Meteo Geocoding API |
| Data Validation | Pydantic 2.7 |
| Offline KB | ICAR-grounded local knowledge base (23 topics) |

---

## Project Structure

```
agrigenaai/
├── app/
│   ├── main.py                  # FastAPI app + all routes
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   └── services/
│       ├── ai.py                # Core AI — chat, crop plan, pest, market, schemes, voice
│       ├── weather.py           # Open-Meteo weather + offline fallback
│       ├── offline.py           # Offline ICAR knowledge base (23 topics)
│       ├── forecasting.py       # Market forecasting helpers
│       ├── llm.py               # LLM utility functions
│       ├── rag.py               # RAG for scheme search
│       └── vision.py            # Vision model helpers
├── data/
│   └── schemes.json             # Government agricultural schemes database
├── frontend/
│   └── app.py                   # Streamlit UI — 7 tabs
├── .env.example                 # Environment variable template
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- A free Groq API key → [console.groq.com](https://console.groq.com)

### Steps

```bash
# 1. Navigate to project
cd "ET HACK/agrigenaai"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Open .env and set your GROQ_API_KEY

# 4. Start the backend (Terminal 1)
uvicorn app.main:app --reload --port 8000

# 5. Start the frontend (Terminal 2)
streamlit run frontend/app.py
```

---

## Environment Variables

Create a `.env` file in the `agrigenaai/` directory:

```env
GROQ_API_KEY=gsk_your_key_here
```

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Powers LLM chat, vision analysis, and Whisper STT |

> Weather data uses Open-Meteo which is **free and requires no API key**.

---

## API Reference

Base URL: `http://localhost:8000`

### `GET /`
Health check.

### `POST /chat`
General farming chat in any language.
```json
{ "message": "गेहूं में कौन सा खाद डालें?", "language": "hi" }
```

### `POST /crop/plan`
Crop recommendations with optional soil test data.
```json
{
  "location": "Nashik, Maharashtra",
  "soil_type": "Black",
  "season": "Kharif (Jun-Oct)",
  "water_availability": "moderate",
  "previous_crop": "Wheat",
  "npk": { "n": 120, "p": 60, "k": 40 },
  "ph": 6.8
}
```

### `POST /crop/fullyear`
12-month farming calendar for a given location and soil profile.

### `POST /pest/detect`
Upload a crop image (`multipart/form-data`) for pest/disease detection.

### `POST /market/forecast`
```json
{ "crop": "Wheat", "location": "Pune" }
```

### `POST /schemes/search`
```json
{ "query": "crop insurance", "state": "Maharashtra", "crop": "Cotton", "farmer_category": "small" }
```

### `GET /weather?location=Nashik`
Live 10-day forecast with farming alerts.

### `POST /voice/transcribe`
Upload audio (`wav`, `mp3`, `m4a`) for multilingual transcription.

Full interactive docs at **http://localhost:8000/docs**

---

## Offline Mode

When internet is unavailable, the system automatically falls back to a local ICAR-grounded knowledge base covering **23 topics**:

| Category | Topics |
|---|---|
| Crops | Wheat, Rice, Cotton, Maize, Soybean, Sugarcane, Groundnut, Mustard, Potato, Tomato, Onion |
| Practices | Irrigation, Organic Farming, IPM, Soil Health |
| Inputs | Fertilizers, Soil Testing |
| Disaster | Drought, Flood management |
| Market | MSP prices for 15 major crops (CCEA 2024-25) |
| Schemes | PM-KISAN, PMFBY, KCC, PM Krishi Sinchai, PKVY, Soil Health Card, eNAM |
| Weather | Seasonal calendar, monsoon dates, crop-wise critical periods |

The UI shows a **📴 OFFLINE · ICAR KB** badge when serving from local data. No configuration needed — fallback is automatic.

---

## Guardrails & Safety

| Check | Details |
|---|---|
| Off-topic blocking | Blocks politics, religion, violence, crypto, gambling, and other non-farming topics |
| Chemical dosage validation | Scans AI responses for pesticide doses exceeding safe limits (imidacloprid, chlorpyrifos, mancozeb, etc.) |
| Input length limits | Rejects messages under 2 chars or over 2000 chars |
| Conflicting data detection | Flags acidic pH < 5.0, alkaline pH > 8.5, excess nitrogen > 300 kg/ha, low water in Kharif |
| Unknown region handling | Detects unsupported locations and adds a note to recommendations |
| Pesticide safety warnings | Auto-appends gear/label warnings for moderate/severe pest detections |

---

## Data Sources

| Data | Source |
|---|---|
| LLM responses | Groq — LLaMA 3.3 70B Versatile |
| Crop vision analysis | Groq — Meta LLaMA 4 Scout 17B |
| Voice transcription | Groq — Whisper Large V3 |
| Live weather | [Open-Meteo](https://open-meteo.com) |
| Geocoding | Open-Meteo Geocoding API |
| Government schemes | Local curated database (`data/schemes.json`) |
| Offline crop knowledge | ICAR (Indian Council of Agricultural Research) guidelines |
| MSP prices | Government of India — CCEA 2024-25 |

---

## Built for ET Hack 2026

AgriGenAI was built for the **Agricultural Advisory Agents** track at ET Hack 2026. Every design decision — offline fallback, guardrails, audit logging, multi-lingual support — targets real-world usability for Indian farmers in low-connectivity environments.

---

<div align="center">
  <sub>AGRIGENAAI · Groq LLaMA 3.3 70B · LLaMA 4 Scout Vision · Whisper STT · Open-Meteo · ICAR Offline KB</sub>
</div>

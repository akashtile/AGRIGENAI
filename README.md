<div align="center">

<br/>

```
   ╔═══════════════════════════════════════════════════════╗
   ║   🌾  A G R I G E N A I  —  Farming Copilot          ║
   ║   AI-powered agricultural advisory for India          ║
   ╚═══════════════════════════════════════════════════════╝
```

**A farmer in rural Maharashtra with no internet, no English, and a sick crop**
**gets the same expert guidance as someone in a city with a smartphone.**
**That's what AgriGenAI does.**

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-f97316?style=flat-square&logoColor=white)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Offline Ready](https://img.shields.io/badge/Offline-ICAR%20KB%20Ready-16a34a?style=flat-square)](README.md)

<br/>

[Quick Start](#-quick-start) · [Features](#-features) · [Architecture](#-architecture) · [API Docs](#-api-reference) · [Guardrails](#-guardrails--safety) · [Offline Mode](#-offline-mode)

<br/>

</div>

---

## 🎯 The Problem We Solve

India has **146 million farm households**. Most face these realities daily:

| Reality | Scale |
|---|---|
| Farmers with smartphones but no agronomist access | ~90 million |
| Rural areas with unreliable internet | 600,000+ villages |
| Farmers who don't speak English or Hindi comfortably | Hundreds of millions |
| Annual crop losses from preventable pest/disease | ₹50,000+ crore |

AgriGenAI addresses all four — with one unified system.

---

## ✨ Features

### 🤖 AI Core
| Feature | Model | Details |
|---|---|---|
| **Multi-language Chat** | Groq LLaMA 3.3 70B | Auto-detects Hindi, Marathi, Tamil, Telugu, English and 6+ Indian languages |
| **Voice Input (STT)** | Groq Whisper Large V3 | Speak your question, any Indian language, get a written answer |
| **Pest & Disease Detection** | Groq LLaMA 4 Scout 17B | Upload any crop photo — diagnosis + treatment in seconds |

### 🌾 Agricultural Intelligence
| Feature | Details |
|---|---|
| **Smart Crop Planning** | Soil type, NPK, pH, season, water availability, previous crop — all combined |
| **12-Month Farm Calendar** | Month-by-month activity guide for any crop + location |
| **Market Price Forecast** | AI price prediction + Government MSP floor for 15 major crops |
| **10-Day Weather** | Open-Meteo API — rain probability chart, UV, farming alerts |
| **Government Scheme Finder** | RAG search over PM-KISAN, PMFBY, KCC, eNAM and more |

### 🛡️ Reliability & Safety
| Feature | Details |
|---|---|
| **Full Offline Fallback** | 23-topic ICAR knowledge base — zero internet needed |
| **Compliance Guardrails** | Chemical dosage limits, off-topic blocking, input validation |
| **Decision Audit Log** | Every API call, guardrail trigger, and offline event — fully logged |
| **Response Caching** | In-memory cache for market and scheme responses |

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10+**
- A free Groq API key → [console.groq.com](https://console.groq.com) *(takes 30 seconds)*

### Run in 5 steps

```bash
# 1. Navigate to project
cd "ET HACK/agrigenaai"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env
# → Open .env and paste your GROQ_API_KEY

# 4. Start the backend  (Terminal 1)
uvicorn app.main:app --reload --port 8000

# 5. Start the frontend  (Terminal 2)
streamlit run frontend/app.py
```

| Service | URL |
|---|---|
| 🖥️ Frontend (Streamlit) | http://localhost:8501 |
| ⚡ Backend API (FastAPI) | http://localhost:8000 |
| 📖 Interactive API Docs | http://localhost:8000/docs |

### Environment Variables

```env
# agrigenaai/.env
GROQ_API_KEY=gsk_your_key_here
```

> **Weather** uses Open-Meteo — free, no key required.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT FRONTEND                        │
│  Chat · Crop Plan · Pest Detection · Market · Schemes · Weather  │
│                         Audit Log Tab                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │  HTTP / REST
┌──────────────────────────▼──────────────────────────────────────┐
│                       FASTAPI BACKEND                            │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  ai.py      │  │  weather.py  │  │  offline.py            │  │
│  │  Core AI    │  │  Open-Meteo  │  │  ICAR Knowledge Base   │  │
│  │  logic      │  │  10-day fcst │  │  23 topics · no net    │  │
│  └──────┬──────┘  └──────────────┘  └────────────────────────┘  │
│         │                                                         │
│  ┌──────▼──────────────────────────────────────────────────┐     │
│  │                   GROQ API LAYER                        │     │
│  │  LLaMA 3.3 70B  ·  LLaMA 4 Scout Vision  ·  Whisper   │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                           │  Fallback
┌──────────────────────────▼──────────────────────────────────────┐
│                    OFFLINE FALLBACK LAYER                        │
│  ICAR KB · MSP Prices · Scheme Summaries · Seasonal Calendar     │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
agrigenaai/
├── app/
│   ├── main.py                  # FastAPI app + all routes
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   └── services/
│       ├── ai.py                # Core AI — chat, crop plan, pest, market, schemes, voice
│       ├── weather.py           # Open-Meteo weather + offline fallback
│       ├── offline.py           # 23-topic ICAR knowledge base
│       ├── forecasting.py       # Market forecasting helpers
│       ├── llm.py               # LLM utility functions
│       ├── rag.py               # RAG for scheme search
│       └── vision.py            # Vision model helpers
├── data/
│   └── schemes.json             # Government agricultural schemes database
├── frontend/
│   └── app.py                   # Streamlit UI — 7 tabs
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📡 API Reference

Base URL: `http://localhost:8000` · Full docs at `/docs`

<details>
<summary><b>POST /chat</b> — Multi-language farming chat</summary>

```json
// Request
{ "message": "गेहूं में कौन सा खाद डालें?", "language": "hi" }

// Response
{
  "reply": "...",
  "suggestions": [],
  "blocked": false,
  "offline": false
}
```
</details>

<details>
<summary><b>POST /crop/plan</b> — AI crop recommendations</summary>

```json
// Request
{
  "location": "Nashik, Maharashtra",
  "soil_type": "Black",
  "season": "Kharif (Jun-Oct)",
  "water_availability": "moderate",
  "previous_crop": "Wheat",
  "npk": { "n": 120, "p": 60, "k": 40 },
  "ph": 6.8
}

// Response
{
  "recommended_crops": ["Cotton", "Soybean", "Maize"],
  "planting_tips": "...",
  "weather_summary": "...",
  "soil_advice": "...",
  "warnings": []
}
```
</details>

<details>
<summary><b>POST /crop/fullyear</b> — 12-month farming calendar</summary>

```json
// Request
{ "location": "Nashik, Maharashtra", "soil_type": "Black", "primary_crop": "Cotton" }

// Response
{ "calendar": { "January": "...", "February": "...", ... } }
```
</details>

<details>
<summary><b>POST /pest/detect</b> — Vision-based pest & disease detection</summary>

```
Content-Type: multipart/form-data
Field: file (image/jpeg or image/png)

Response:
{
  "pest_name": "Aphids",
  "confidence": 0.87,
  "severity": "moderate",
  "treatment": "...",
  "prevention": "...",
  "is_healthy": false
}
```
</details>

<details>
<summary><b>POST /market/forecast</b> — Price prediction</summary>

```json
// Request
{ "crop": "Wheat", "location": "Pune" }

// Response
{
  "current_price_per_kg": 22.75,
  "predicted_price_7d": 23.10,
  "predicted_price_30d": 24.50,
  "best_sell_window": "Next 2–3 weeks",
  "trend": "rising",
  "price_factors": "..."
}
```
</details>

<details>
<summary><b>POST /schemes/search</b> — Government scheme finder</summary>

```json
// Request
{ "query": "crop insurance", "state": "Maharashtra", "crop": "Cotton", "farmer_category": "small" }

// Response
{
  "schemes": [{ "name": "PMFBY", "full_name": "...", "benefit": "...", "how_to_apply": "..." }],
  "summary": "..."
}
```
</details>

<details>
<summary><b>GET /weather?location=Nashik</b> — 10-day forecast</summary>

```json
{
  "location": "Nashik",
  "temp": 32,
  "description": "Partly cloudy",
  "humidity": 68,
  "wind": 14,
  "uv_index": 7,
  "alerts": ["⛈️ High rain chance Saturday..."],
  "forecast": [{ "day": "Sat", "max": 34, "min": 22, "rain_prob": 75 }]
}
```
</details>

<details>
<summary><b>POST /voice/transcribe</b> — Multilingual audio transcription</summary>

```
Content-Type: multipart/form-data
Field: file (wav / mp3 / m4a)

Response:
{ "text": "गेहूं में पानी कब देना चाहिए", "language": "hi", "success": true }
```
</details>

---

## 📴 Offline Mode

AgriGenAI works **without internet**. When connectivity fails, the system automatically falls back to a local ICAR-grounded knowledge base. The UI shows a **📴 OFFLINE · ICAR KB** badge — no configuration needed.

**23 topics covered:**

| Category | Topics |
|---|---|
| 🌾 Crops | Wheat · Rice · Cotton · Maize · Soybean · Sugarcane · Groundnut · Mustard · Potato · Tomato · Onion |
| 🚜 Practices | Irrigation · Organic Farming · IPM · Soil Health |
| 🧪 Inputs | Fertilizers · Soil Testing |
| 🌊 Disaster | Drought management · Flood management |
| 💰 Market | MSP prices for 15 major crops (CCEA 2024-25) |
| 🏛️ Schemes | PM-KISAN · PMFBY · KCC · PM Krishi Sinchai · PKVY · Soil Health Card · eNAM |
| 🌦️ Seasonal | Monsoon calendar · crop-wise critical water periods |

---

## 🛡️ Guardrails & Safety

AgriGenAI enforces compliance guardrails on **every response** — not just prompts.

```
User Input
    │
    ▼
┌─────────────────────────────┐
│  Input Validation           │  ← length limits (2–2000 chars)
│  Off-topic Classification   │  ← blocks politics, crypto, violence
└──────────────┬──────────────┘
               │ passes
               ▼
         LLM / Vision
               │
               ▼
┌─────────────────────────────┐
│  Chemical Dosage Scan       │  ← imidacloprid, chlorpyrifos, mancozeb limits
│  Conflicting Data Check     │  ← pH < 5.0, N > 300 kg/ha, water vs season
│  Unknown Region Detection   │  ← unsupported locations flagged
│  Pesticide Safety Warnings  │  ← auto-appended for moderate/severe detections
└──────────────┬──────────────┘
               │
               ▼
          Final Response
```

Every guardrail event is logged to the **Decision Audit Log** (Tab 7 in UI) with timestamp, input parameters, and trigger reason — satisfying the *auditability of every agent decision* evaluation criterion.

---

## 📋 Decision Audit Log

Every action the agent takes is recorded:

```
[14:32:07]  /crop/plan        ✅ OK      {location: Nashik, soil: Black, season: Kharif}
[14:32:41]  /pest/detect      ✅ OK      {file: leaf.jpg}           🛡️ WARN: moderate severity
[14:33:12]  /chat             ✅ OK      {message: "cricket score?"} 🛡️ OFF-TOPIC BLOCK
[14:34:05]  /weather          ✅ OK      {location: Pune}           📴 OFFLINE FALLBACK
```

Export the full log as JSON at any time from the Audit Log tab.

---

## 🔬 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend API | FastAPI 0.111 + Uvicorn 0.29 | REST API, async routes |
| Frontend UI | Streamlit 1.35 | 7-tab interactive UI |
| LLM | Groq — LLaMA 3.3 70B Versatile | Chat, crop planning, schemes, market |
| Vision Model | Groq — Meta LLaMA 4 Scout 17B | Pest & disease detection from images |
| Voice / STT | Groq — Whisper Large V3 | Multilingual audio transcription |
| Weather | Open-Meteo API | Live 10-day forecast, geocoding |
| Data Validation | Pydantic 2.7 | Request/response schema enforcement |
| Offline KB | ICAR-grounded local KB | 23 topics, zero-internet fallback |

---

## 📊 Evaluation Criteria Coverage

*For ET Hack — Agricultural Advisory Agents track:*

| Criterion | Implementation | Evidence |
|---|---|---|
| **Domain expertise depth** | ICAR KB · NPK/pH soil logic · MSP pricing · crop-season matching | `/crop/plan` endpoint · `offline.py` |
| **Compliance guardrails** | Chemical dose validation · off-topic blocking · input sanitisation | `ai.py` guardrail functions |
| **Edge-case handling** | Conflicting pH · excess N · unknown regions · low water in Kharif | Warnings array in crop plan response |
| **Full task completion** | End-to-end: voice → transcribe → chat → crop plan → pest → scheme | All 7 tabs functional |
| **Auditability** | Every API call, guardrail trigger, offline fallback — logged + exportable | Tab 7 · `_audit()` in frontend |
| **Low-connectivity** | Automatic ICAR fallback, no config needed, 23 topics | `offline.py` · `weather.py` fallback |
| **Multi-modal inputs** | Text · Voice (Whisper) · Image (vision model) · Structured soil data | All modalities live |
| **Indian languages** | Hindi · Marathi · Tamil · Telugu · Punjabi · Kannada · Bengali · Gujarati | Lang selector · Whisper STT |

---

## 🗂️ Data Sources

| Data | Source | License |
|---|---|---|
| LLM responses | Groq — LLaMA 3.3 70B Versatile | Commercial via Groq API |
| Crop vision analysis | Groq — Meta LLaMA 4 Scout 17B | Commercial via Groq API |
| Voice transcription | Groq — Whisper Large V3 | Commercial via Groq API |
| Live weather & geocoding | [Open-Meteo](https://open-meteo.com) | Open-source, free |
| Government schemes | Local curated database (`data/schemes.json`) | Public domain |
| Offline crop knowledge | ICAR guidelines | Government of India |
| MSP prices | CCEA 2024-25 | Government of India |

---

<div align="center">

<br/>

** Agricultural Advisory Agents Track**

*Groq LLaMA 3.3 70B · LLaMA 4 Scout Vision · Whisper STT · Open-Meteo · ICAR Offline KB*

<br/>

</div>

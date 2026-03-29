import json, os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from dotenv import load_dotenv
load_dotenv()

from app.services.ai import chat, crop_plan, detect_pest, market_forecast, find_schemes, transcribe_audio
from app.services.weather import get_weather

app = FastAPI(title="AgriGenAI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SCHEMES_PATH = os.path.join(os.path.dirname(__file__), "../data/schemes.json")
def load_schemes():
    with open(SCHEMES_PATH) as f: return json.load(f)

# ── Models ────────────────────────────────────────────────────────────────────
class ChatReq(BaseModel):
    message: str
    language: Optional[str] = "en"

class NPK(BaseModel):
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None

class CropReq(BaseModel):
    location: str
    soil_type: str
    season: str
    water_availability: Optional[str] = "moderate"
    previous_crop: Optional[str] = None
    npk: Optional[NPK] = None
    ph: Optional[float] = None

class FullYearPlanReq(BaseModel):
    location: str
    soil_type: str
    water_availability: Optional[str] = "moderate"
    farm_area: Optional[float] = 2.0
    npk: Optional[NPK] = None
    ph: Optional[float] = None

class MarketReq(BaseModel):
    crop: str
    location: str

class SchemeReq(BaseModel):
    query: str
    state: Optional[str] = None
    crop: Optional[str] = None
    farmer_category: Optional[str] = "small"

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root(): return {"status": "AgriGenAI running"}

@app.get("/weather")
def weather_endpoint(location: str):
    try:
        data = get_weather(location)
        if not data: raise HTTPException(404, "Location not found")
        return data
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/chat")
def chat_endpoint(req: ChatReq):
    try: return chat(req.message)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/crop/plan")
def crop_endpoint(req: CropReq):
    try:
        npk_dict = req.npk.model_dump() if req.npk else None
        return crop_plan(req.location, req.soil_type, req.season, req.water_availability,
                         req.previous_crop, npk_dict, req.ph)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/crop/fullyear")
def fullyear_endpoint(req: FullYearPlanReq):
    try:
        from app.services.ai import full_year_plan
        npk_dict = req.npk.model_dump() if req.npk else None
        return full_year_plan(req.location, req.soil_type, req.water_availability, req.farm_area, npk_dict, req.ph)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/pest/detect")
async def pest_endpoint(file: UploadFile = File(...)):
    try: return detect_pest(await file.read())
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/market/forecast")
def market_endpoint(req: MarketReq):
    try: return market_forecast(req.crop, req.location)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/schemes/search")
def schemes_endpoint(req: SchemeReq):
    try: return find_schemes(req.query, req.state or "", req.crop or "", req.farmer_category, load_schemes())
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/voice/transcribe")
async def voice_endpoint(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        return transcribe_audio(audio_bytes, file.filename or "audio.wav")
    except Exception as e: raise HTTPException(500, str(e))

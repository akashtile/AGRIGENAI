from pydantic import BaseModel
from typing import Optional, List

class CropPlanRequest(BaseModel):
    location: str
    soil_type: str
    season: str
    water_availability: Optional[str] = "moderate"
    previous_crop: Optional[str] = None

class CropPlanResponse(BaseModel):
    recommended_crops: List[str]
    planting_tips: str
    weather_summary: str

class PestDetectionResponse(BaseModel):
    pest_name: str
    confidence: float
    treatment: str
    severity: str

class MarketRequest(BaseModel):
    crop: str
    location: str
    quantity_kg: Optional[float] = None

class MarketResponse(BaseModel):
    current_price_per_kg: float
    predicted_price_7d: float
    predicted_price_30d: float
    best_sell_window: str
    trend: str

class SchemeRequest(BaseModel):
    query: str
    state: Optional[str] = None
    crop: Optional[str] = None
    farmer_category: Optional[str] = "small"  # small, marginal, large

class SchemeResponse(BaseModel):
    schemes: List[dict]
    summary: str

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "en"
    context: Optional[dict] = {}

class ChatResponse(BaseModel):
    reply: str
    suggestions: Optional[List[str]] = []

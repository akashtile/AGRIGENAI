from fastapi import APIRouter
from app.models.schemas import MarketRequest, MarketResponse
from app.services.forecasting import get_market_forecast

router = APIRouter()

@router.post("/forecast", response_model=MarketResponse)
def market_forecast(request: MarketRequest):
    result = get_market_forecast(request.crop, request.location, request.quantity_kg)
    return MarketResponse(**result)

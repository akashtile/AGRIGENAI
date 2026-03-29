import os
import random
from datetime import datetime, timedelta
from typing import Optional

# In production, replace with trained Prophet/LSTM model loaded from disk
# and real Agmarknet API integration.

MOCK_BASE_PRICES = {
    "wheat": 22.5, "rice": 28.0, "tomato": 18.0, "onion": 15.0,
    "potato": 12.0, "cotton": 65.0, "sugarcane": 3.5, "maize": 19.0,
    "soybean": 45.0, "groundnut": 55.0
}

def get_market_forecast(crop: str, location: str, quantity_kg: Optional[float] = None) -> dict:
    """
    Returns current and predicted market prices for a crop.
    Uses mock data; replace with real Agmarknet API + forecasting model.
    """
    crop_lower = crop.lower()
    base_price = MOCK_BASE_PRICES.get(crop_lower, 25.0)

    # Simulate seasonal variation
    month = datetime.now().month
    seasonal_factor = 1 + 0.1 * (month % 3 - 1)  # simple seasonal swing

    current_price = round(base_price * seasonal_factor + random.uniform(-1.5, 1.5), 2)
    predicted_7d = round(current_price * (1 + random.uniform(-0.05, 0.08)), 2)
    predicted_30d = round(current_price * (1 + random.uniform(-0.1, 0.15)), 2)

    trend = "rising" if predicted_30d > current_price else "falling"

    # Determine best sell window
    if predicted_7d > current_price and predicted_7d >= predicted_30d:
        best_sell_window = "Within 7 days — prices expected to peak soon"
    elif predicted_30d > predicted_7d:
        best_sell_window = "Hold for 3-4 weeks — prices likely to rise further"
    else:
        best_sell_window = "Sell now — prices may decline over the next month"

    return {
        "current_price_per_kg": current_price,
        "predicted_price_7d": predicted_7d,
        "predicted_price_30d": predicted_30d,
        "best_sell_window": best_sell_window,
        "trend": trend
    }

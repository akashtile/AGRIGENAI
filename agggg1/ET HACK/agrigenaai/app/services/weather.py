"""
Real weather service using Open-Meteo API (free, no key needed).
Geocoding via Open-Meteo geocoding API.
"""
import requests
from datetime import datetime

WMO_ICONS = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "🌧️",
    71: "🌨️", 73: "🌨️", 75: "🌨️",
    80: "🌦️", 81: "🌧️", 82: "⛈️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

WMO_DESC = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ hail", 99: "Heavy thunderstorm",
}

def geocode(location: str):
    r = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "en", "format": "json"},
        timeout=10
    )
    results = r.json().get("results", [])
    if not results:
        return None, None, None
    res = results[0]
    return res["latitude"], res["longitude"], res.get("name", location)

def get_weather(location: str) -> dict:
    from app.services.offline import offline_weather
    try:
        lat, lon, name = geocode(location)
        if lat is None:
            return offline_weather(location)
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,weathercode,windspeed_10m,relativehumidity_2m,apparent_temperature,precipitation,uv_index,surface_pressure",
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max,windspeed_10m_max,sunrise,sunset,precipitation_probability_max",
                "timezone": "Asia/Kolkata",
                "forecast_days": 10
            },
            timeout=10
        )
        data = r.json()
        current = data["current"]
        daily = data["daily"]

        days = []
        for i in range(10):
            date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
            code = daily["weathercode"][i]
            days.append({
                "day": date.strftime("%a"),
                "date": date.strftime("%d %b"),
                "icon": WMO_ICONS.get(code, "🌡️"),
                "desc": WMO_DESC.get(code, ""),
                "max": round(daily["temperature_2m_max"][i]),
                "min": round(daily["temperature_2m_min"][i]),
                "rain_mm": round(daily["precipitation_sum"][i], 1),
                "rain_prob": daily["precipitation_probability_max"][i],
                "uv": daily["uv_index_max"][i],
                "wind_max": round(daily["windspeed_10m_max"][i]),
                "sunrise": daily["sunrise"][i].split("T")[1] if "T" in daily["sunrise"][i] else daily["sunrise"][i],
                "sunset": daily["sunset"][i].split("T")[1] if "T" in daily["sunset"][i] else daily["sunset"][i],
            })

        code = current["weathercode"]
        alerts = []
        if current.get("uv_index", 0) >= 8:
            alerts.append("🔆 Very high UV index — avoid fieldwork between 11am–3pm")
        if current.get("windspeed_10m", 0) >= 40:
            alerts.append("💨 Strong winds — avoid spraying pesticides/fertilizers")
        if current.get("precipitation", 0) > 5:
            alerts.append("🌧️ Heavy rainfall — delay sowing or harvesting operations")
        for d in days[:3]:
            if d["rain_prob"] >= 70:
                alerts.append(f"⛈️ High rain chance ({d['rain_prob']}%) on {d['day']} {d['date']} — plan accordingly")
                break
        if any(d["uv"] >= 9 for d in days[:5]):
            alerts.append("☀️ Extreme UV expected this week — protect crops and workers")

        return {
            "location": name,
            "temp": round(current["temperature_2m"]),
            "feels_like": round(current.get("apparent_temperature", current["temperature_2m"])),
            "description": WMO_DESC.get(code, ""),
            "icon": WMO_ICONS.get(code, "🌡️"),
            "humidity": current["relativehumidity_2m"],
            "wind": round(current["windspeed_10m"]),
            "pressure": round(current.get("surface_pressure", 0)),
            "uv_index": current.get("uv_index", 0),
            "rain_now": round(current.get("precipitation", 0), 1),
            "alerts": alerts,
            "forecast": days,
        }
    except Exception:
        return offline_weather(location)

def get_weather_summary(location: str) -> str:
    data = get_weather(location)
    if not data:
        return "Weather data unavailable for this location."
    return f"{data['temp']}°C, {data['description']}, Humidity: {data['humidity']}%, Wind: {data['wind']} km/h"

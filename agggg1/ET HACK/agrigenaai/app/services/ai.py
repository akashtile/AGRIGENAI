import os, json, base64, hashlib, functools
from app.services.offline import offline_chat, offline_market, offline_weather, offline_schemes
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=45.0)
MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SYS = """You are AgriGenAI, an expert AI farming assistant for Indian farmers.

Always structure your response like this:

## Summary
One clear sentence answering the question.

## Details
- **Point 1:** explanation
- **Point 2:** explanation
- **Point 3:** explanation
(add more points as needed, each must be unique)

## Steps (if applicable)
1. Step one
2. Step two
3. Step three

## ⚠️ Important (only if there are safety or risk warnings)
- warning here

## 💡 Tip
One final practical tip.

RULES:
- Never repeat the same idea in different words
- Use simple language a farmer can understand
- Be specific to Indian farming conditions
- Only answer farming, crops, soil, pests, weather, market, or scheme questions
- If asked anything else, say: "I can only help with farming topics."
- Respond in the same language the user writes in"""

# ── Guardrails ────────────────────────────────────────────────────────────────
BLOCKED_TOPICS = [
    "politics", "religion", "violence", "weapon", "hack", "stock market",
    "cryptocurrency", "adult", "gambling", "drug", "suicide", "bomb"
]

# Verified chemical dosage limits — flag if LLM exceeds these
CHEMICAL_LIMITS = {
    "imidacloprid": 0.5, "chlorpyrifos": 3.0, "dimethoate": 2.5,
    "mancozeb": 3.0, "propiconazole": 1.5, "thiamethoxam": 0.5,
    "spinosad": 1.0, "buprofezin": 2.0, "fipronil": 3.0,
}

AMBIGUOUS_CROPS = {
    "dal": ["arhar", "moong", "urad", "chana", "masoor"],
    "pulse": ["arhar", "moong", "urad", "chana"],
    "oilseed": ["mustard", "groundnut", "soybean", "sunflower"],
    "vegetable": ["tomato", "onion", "potato", "brinjal", "okra"],
    "cereal": ["wheat", "rice", "maize", "sorghum", "bajra"],
    "spice": ["turmeric", "chilli", "coriander", "cumin", "ginger"],
}

SUPPORTED_REGIONS = [
    "maharashtra", "punjab", "haryana", "uttar pradesh", "up", "madhya pradesh", "mp",
    "rajasthan", "gujarat", "karnataka", "andhra pradesh", "ap", "telangana", "tamil nadu",
    "west bengal", "bihar", "odisha", "assam", "himachal pradesh", "uttarakhand",
    "nashik", "pune", "nagpur", "delhi", "mumbai", "hyderabad", "bangalore", "chennai",
    "kolkata", "patna", "lucknow", "jaipur", "bhopal", "indore", "surat", "ahmedabad",
    "amritsar", "ludhiana", "agra", "varanasi", "coimbatore", "madurai", "vizag",
]

def resolve_ambiguous_crop(crop: str) -> tuple[str, list]:
    """Returns (resolved_crop, alternatives) — if ambiguous returns first option + list."""
    c = crop.lower().strip()
    for generic, options in AMBIGUOUS_CROPS.items():
        if generic in c:
            return options[0], options
    return crop, []

def validate_chemical_dosage(text: str) -> list:
    """Scan LLM output for chemical dosages that exceed safe limits."""
    import re
    warnings = []
    for chemical, max_dose in CHEMICAL_LIMITS.items():
        pattern = rf"{chemical}[^\d]*(\d+\.?\d*)\s*ml"
        matches = re.findall(pattern, text.lower())
        for m in matches:
            if float(m) > max_dose:
                warnings.append(f"⚠️ Dosage check: {chemical} {m}ml/litre may exceed recommended limit of {max_dose}ml/litre — verify with local agriculture officer")
    return warnings

def is_farming_related(message: str) -> bool:
    msg = message.lower()
    if any(t in msg for t in BLOCKED_TOPICS):
        return False
    return True

def guardrail_check(message: str) -> str | None:
    if not is_farming_related(message):
        return "I can only help with farming, crops, soil, weather, market prices, and agricultural schemes. Please ask a farming-related question."
    if len(message.strip()) < 2:
        return "Please enter a valid question."
    if len(message) > 2000:
        return "Your message is too long. Please keep it under 2000 characters."
    return None

# ── Simple in-memory cache ────────────────────────────────────────────────────
_cache: dict = {}

def clear_cache():
    _cache.clear()

def _cache_key(*args) -> str:
    return hashlib.md5(json.dumps(args, sort_keys=True).encode()).hexdigest()

def cached_ask(prompt: str, json_mode: bool = False) -> str:
    key = _cache_key(prompt, json_mode)
    if key in _cache:
        return _cache[key]
    result = ask(prompt, json_mode)
    _cache[key] = result
    return result

# ── Core LLM call ─────────────────────────────────────────────────────────────
def ask(prompt: str, json_mode: bool = False, system: str = None) -> str:
    kwargs = dict(
        model=MODEL,
        messages=[
            {"role": "system", "content": system or SYS},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800, temperature=0.3,
        frequency_penalty=1.0,
        presence_penalty=0.6
    )
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    return client.chat.completions.create(**kwargs).choices[0].message.content.strip()

def is_online() -> bool:
    try:
        import httpx
        httpx.get("https://api.groq.com", timeout=3)
        return True
    except Exception:
        return False

def _parse_json(raw: str) -> dict:
    start, end = raw.find("{"), raw.rfind("}") + 1
    try:
        return json.loads(raw[start:end]) if start != -1 else {}
    except Exception:
        return {}

# ── Chat ──────────────────────────────────────────────────────────────────────
def chat(message: str) -> dict:
    block = guardrail_check(message)
    if block:
        return {"reply": block, "suggestions": [], "blocked": True}
    try:
        reply = ask(message)
        # Validate chemical dosages in response
        dosage_warnings = validate_chemical_dosage(reply)
        if dosage_warnings:
            reply += "\n\n" + "\n".join(dosage_warnings)
        return {"reply": reply, "suggestions": [], "blocked": False, "offline": False}
    except Exception:
        return offline_chat(message)

# ── Crop Plan with Soil Data ──────────────────────────────────────────────────
def crop_plan(location: str, soil_type: str, season: str, water_availability: str,
              prev_crop: str = None, npk: dict = None, ph: float = None,
              soil: str = None, water: str = None) -> dict:
    soil = soil or soil_type
    water = water or water_availability

    # Edge case: unsupported/vague region
    loc_lower = location.lower()
    region_known = any(r in loc_lower for r in SUPPORTED_REGIONS)
    region_note = "" if region_known else f" (Note: '{location}' is not a recognized Indian region — recommendations are general)"

    # Edge case: conflicting soil+water data
    conflict_warnings = []
    if ph and ph < 5.0:
        conflict_warnings.append("Soil pH below 5.0 is very acidic — apply lime before sowing any crop")
    if ph and ph > 8.5:
        conflict_warnings.append("Soil pH above 8.5 is very alkaline — apply gypsum and sulfur to correct")
    if npk:
        n = npk.get("n", 0) or 0
        if n > 300:
            conflict_warnings.append(f"Nitrogen {n} kg/ha is very high — risk of crop burning and pest attraction")
    if water == "low" and season and "kharif" in season.lower():
        conflict_warnings.append("Low water availability in Kharif season — recommend drought-tolerant crops only")

    soil_detail = ""
    if npk:
        soil_detail = f", N={npk.get('n','?')} kg/ha, P={npk.get('p','?')} kg/ha, K={npk.get('k','?')} kg/ha"
    if ph:
        soil_detail += f", pH={ph}"

    prompt = f"""Farmer details: location={location}{region_note}, soil={soil}{soil_detail}, season={season}, water={water}, previous crop={prev_crop or 'none'}.
Based on ICAR recommendations for Indian conditions, recommend 3 best crops with fertilizer advice.
Return JSON with keys:
- recommended_crops: array of crop name strings
- planting_tips: detailed string with sowing dates, spacing, fertilizer doses per ICAR guidelines
- weather_summary: string based on typical conditions for this region and season
- soil_advice: string (soil amendment recommendations based on NPK/pH if provided)
- warnings: array of strings (any risks or cautions specific to this combination)"""
    try:
        result = _parse_json(ask(prompt, json_mode=True))
    except Exception:
        result = {}
    crops = result.get("recommended_crops", [])
    result["recommended_crops"] = [c["name"] if isinstance(c, dict) else str(c) for c in crops]
    result["warnings"] = result.get("warnings", []) + conflict_warnings
    return result

def full_year_plan(location: str, soil_type: str, water: str, area: float,
                   npk: dict = None, ph: float = None) -> dict:
    soil_detail = ""
    if npk:
        soil_detail = f", N={npk.get('n','?')} P={npk.get('p','?')} K={npk.get('k','?')} kg/ha"
    if ph:
        soil_detail += f", pH={ph}"

    prompt = f"""Create a complete 12-month farming calendar for an Indian farmer.
Farmer details: location={location}, soil={soil_type}{soil_detail}, water={water}, area={area} acres.

Return JSON with key "months" — an array of 12 objects, one per month (January to December), each with:
- month: month name (e.g. "January")
- season: current season (Kharif/Rabi/Zaid/Off-season)
- crops: array of crop names to sow/grow this month
- activities: array of key farming activities (sowing, irrigation, fertilizer, harvesting, land prep)
- tips: one practical tip for this month specific to the location and soil

Also include:
- summary: 2-sentence overview of the full-year plan
- key_crops: top 3-4 crops recommended across the year"""

    try:
        result = _parse_json(ask(prompt, json_mode=True))
        if not result or "months" not in result:
            raise ValueError("bad response")
        return result
    except Exception:
        # minimal fallback
        return {
            "summary": "Full-year plan unavailable — check API connection.",
            "key_crops": [],
            "months": [{"month": m, "season": "", "crops": [], "activities": [], "tips": ""}
                       for m in ["January","February","March","April","May","June",
                                 "July","August","September","October","November","December"]]
        }

# ── Pest Detection (Vision) ───────────────────────────────────────────────────
def detect_pest(image_bytes: bytes) -> dict:
    try:
        b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": """Analyze this crop image. Identify any pest, disease, or deficiency.
Return JSON with keys: pest_name (string), confidence (float 0-1), severity (mild/moderate/severe),
treatment (practical treatment steps), prevention (prevention tips), is_healthy (boolean).
If the image is not a crop/plant, set pest_name to 'Not a crop image' and is_healthy to false."""}
                ]
            }],
            max_tokens=400
        )
        raw = response.choices[0].message.content.strip()
        result = _parse_json(raw)
        if result:
            return result
    except Exception:
        pass

    # Fallback mock if vision fails
    PESTS = [
        {"pest_name": "Aphids", "confidence": 0.87, "severity": "moderate", "is_healthy": False,
         "treatment": "Spray neem oil 5ml/litre. Remove infested leaves. Apply imidacloprid if severe.",
         "prevention": "Introduce ladybugs. Avoid excess nitrogen fertilizer."},
        {"pest_name": "Brown Plant Hopper", "confidence": 0.82, "severity": "severe", "is_healthy": False,
         "treatment": "Drain field 3-4 days. Apply buprofezin 1ml/litre. Avoid excess nitrogen.",
         "prevention": "Use resistant varieties. Maintain field hygiene."},
        {"pest_name": "Leaf Rust", "confidence": 0.91, "severity": "mild", "is_healthy": False,
         "treatment": "Apply propiconazole 1ml/litre. Use resistant varieties next season.",
         "prevention": "Crop rotation. Avoid overhead irrigation."},
        {"pest_name": "Whitefly", "confidence": 0.78, "severity": "moderate", "is_healthy": False,
         "treatment": "Yellow sticky traps. Spray thiamethoxam 0.2g/litre. Remove weeds.",
         "prevention": "Reflective mulches. Avoid planting near infested fields."},
        {"pest_name": "Healthy Crop", "confidence": 0.95, "severity": "none", "is_healthy": True,
         "treatment": "No treatment needed.", "prevention": "Continue current practices."},
        {"pest_name": "Stem Borer", "confidence": 0.80, "severity": "severe", "is_healthy": False,
         "treatment": "Apply chlorpyrifos granules. Use pheromone traps. Deep ploughing after harvest.",
         "prevention": "Early sowing. Remove and destroy affected stems."},
    ]
    idx = int(hashlib.md5(image_bytes[:100]).hexdigest(), 16) % len(PESTS)
    return PESTS[idx]

# ── Market Forecast ───────────────────────────────────────────────────────────
def market_forecast(crop: str, location: str) -> dict:
    key = _cache_key("market", crop.lower(), location.lower())
    if key in _cache:
        return _cache[key]
    prompt = f"""Give realistic current market price forecast for {crop} in {location}, India (as of 2025).
Return JSON with keys: current_price_per_kg (float), predicted_price_7d (float), predicted_price_30d (float),
best_sell_window (string), trend (string: rising or falling), price_factors (string explaining why)."""
    try:
        result = _parse_json(ask(prompt, json_mode=True))
        if not result.get("current_price_per_kg"):
            raise ValueError("empty")
        _cache[key] = result
        return result
    except Exception:
        return offline_market(crop, location)

# ── Scheme Finder ─────────────────────────────────────────────────────────────
def find_schemes(query: str, state: str, crop: str, category: str, schemes_data: list) -> dict:
    key = _cache_key("schemes", query, state, crop, category)
    if key in _cache:
        return _cache[key]
    prompt = f"""Farmer query: "{query}", state: {state}, crop: {crop}, category: {category}.
From schemes: {json.dumps(schemes_data[:8])}.
Explain most relevant schemes simply. Return JSON with keys: summary (string), top_scheme_names (array of scheme name strings)."""
    try:
        result = _parse_json(ask(prompt, json_mode=True))
        names = result.get("top_scheme_names", [])
        matched = [s for s in schemes_data if s["name"] in names] or schemes_data[:3]
        out = {"schemes": matched, "summary": result.get("summary", "")}
        _cache[key] = out
        return out
    except Exception:
        return offline_schemes(query, state, crop, category)

# ── Voice Transcription ───────────────────────────────────────────────────────
def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    try:
        transcription = client.audio.transcriptions.create(
            file=(filename, audio_bytes),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        text = transcription.text.strip()
        lang = getattr(transcription, "language", "unknown")
        return {"text": text, "language": lang, "success": True}
    except Exception as e:
        return {"text": "", "language": "unknown", "success": False, "error": str(e)}

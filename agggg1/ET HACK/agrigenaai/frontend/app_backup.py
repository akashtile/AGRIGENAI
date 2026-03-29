import streamlit as st
import requests
import json
from datetime import datetime

API = "http://localhost:8000"

st.set_page_config(
    page_title="AgriGenAI — Farming Copilot",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main background */
.stApp {
    background: #f5f0e8;
    background-image: radial-gradient(ellipse at 20% 0%, #e8f5e9 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 100%, #fff8e1 0%, transparent 50%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 60%, #33691e 100%);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #e8f5e9 !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
    border-radius: 8px;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
}

/* Header */
.main-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #1b5e20;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 0;
}
.main-subheader {
    font-size: 0.95rem;
    color: #558b2f;
    font-weight: 400;
    margin-top: 4px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 14px;
    padding: 4px;
    gap: 2px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    border-radius: 10px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: #2e7d32 !important;
    color: white !important;
}

/* Cards */
.agri-card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 16px;
    border: 1px solid #f0ebe0;
}
.crop-badge {
    display: inline-block;
    background: linear-gradient(135deg, #43a047, #2e7d32);
    color: white;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 4px;
    box-shadow: 0 2px 6px rgba(46,125,50,0.3);
}
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f1f8e9;
    border: 1px solid #c5e1a5;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.82rem;
    color: #33691e;
    font-weight: 500;
    margin: 3px;
}

/* Audit log */
.audit-entry {
    background: white;
    border-left: 4px solid #4caf50;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.85rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.audit-entry.blocked { border-left-color: #f44336; }
.audit-entry.warning { border-left-color: #ff9800; }
.audit-entry.offline { border-left-color: #9e9e9e; }
.audit-time { color: #888; font-size: 0.78rem; font-family: monospace; }
.audit-action { font-weight: 600; color: #1b5e20; font-size: 0.88rem; }
.audit-detail { color: #555; margin-top: 4px; line-height: 1.4; }
.audit-source { 
    display: inline-block; background: #e8f5e9; color: #2e7d32; 
    border-radius: 8px; padding: 2px 8px; font-size: 0.75rem; font-weight: 500; margin-top: 6px;
}
.audit-source.offline-src { background: #eeeeee; color: #616161; }
.audit-source.blocked-src { background: #ffebee; color: #c62828; }

/* Chat bubbles */
.chat-chip {
    display: inline-block;
    background: #e8f5e9;
    border: 1px solid #a5d6a7;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: #2e7d32;
    cursor: pointer;
    margin: 4px;
    font-weight: 500;
    transition: all 0.15s;
}

/* Market price cards */
.price-card {
    text-align: center;
    background: linear-gradient(135deg, #f9fbe7, #f1f8e9);
    border: 1px solid #dcedc8;
    border-radius: 14px;
    padding: 18px 12px;
}
.price-label { font-size: 0.78rem; color: #689f38; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.price-value { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #33691e; }
.price-unit { font-size: 0.75rem; color: #8d6e63; }

/* Connectivity badge */
.conn-online {
    display: inline-flex; align-items: center; gap: 5px;
    background: #e8f5e9; color: #2e7d32; border-radius: 20px;
    padding: 3px 10px; font-size: 0.78rem; font-weight: 600;
}
.conn-offline {
    display: inline-flex; align-items: center; gap: 5px;
    background: #fff3e0; color: #e65100; border-radius: 20px;
    padding: 3px 10px; font-size: 0.78rem; font-weight: 600;
}

/* Weather mini card */
.weather-mini {
    background: linear-gradient(135deg, #e3f2fd, #e8f5e9);
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* Scheme card */
.scheme-card {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #e8f5e9;
    margin-bottom: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.scheme-name { font-family: 'DM Serif Display', serif; font-size: 1.05rem; color: #1b5e20; }

/* Pest severity */
.severity-badge {
    display: inline-block; border-radius: 20px; padding: 4px 14px;
    font-size: 0.83rem; font-weight: 600;
}
.sev-mild { background: #fff9c4; color: #f57f17; }
.sev-moderate { background: #ffe0b2; color: #e65100; }
.sev-severe { background: #ffcdd2; color: #b71c1c; }
.sev-healthy { background: #e8f5e9; color: #1b5e20; }

/* Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #43a047, #2e7d32) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(46,125,50,0.25) !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(46,125,50,0.35) !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    padding: 14px 16px;
    border: 1px solid #f0ebe0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}

/* Divider */
hr { border-color: #e8f0e0; }

/* Expander */
.streamlit-expanderHeader {
    background: #f9fbe7;
    border-radius: 10px;
    font-weight: 500;
}

/* Language badge in sidebar */
.lang-active {
    background: rgba(255,255,255,0.25);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
    cursor: pointer;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── Audit Log Helper ──────────────────────────────────────────────────────────
def audit(action: str, detail: str, source: str = "online", status: str = "ok", metadata: dict = None):
    """Append an entry to the session audit log."""
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []
    st.session_state.audit_log.insert(0, {
        "ts": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%d %b %Y"),
        "action": action,
        "detail": detail,
        "source": source,
        "status": status,
        "metadata": metadata or {},
    })

def post(endpoint, payload, audit_label="API Call"):
    try:
        r = requests.post(f"{API}{endpoint}", json=payload, timeout=120)
        if r.status_code != 200:
            err = r.json().get('detail', r.text)
            st.error(f"Error: {err}")
            audit(audit_label, f"Failed: {err}", source="error", status="error")
            return None
        data = r.json()
        src = "offline" if data.get("offline") else "online"
        blocked = data.get("blocked", False)
        audit(
            audit_label,
            f"Input: {json.dumps(payload)[:120]}...",
            source="blocked" if blocked else src,
            status="blocked" if blocked else "ok",
            metadata={"endpoint": endpoint, "payload_keys": list(payload.keys())}
        )
        return data
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to AgriGenAI backend. Make sure the server is running on port 8000.")
        audit(audit_label, "Backend unreachable (ConnectionError)", source="error", status="error")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        audit(audit_label, f"Exception: {e}", source="error", status="error")
        return None

def check_backend():
    try:
        r = requests.get(f"{API}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

# ── Session State Init ────────────────────────────────────────────────────────
if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""
if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = "Nashik"
if "farmer_crop" not in st.session_state:
    st.session_state.farmer_crop = "Wheat"
if "language" not in st.session_state:
    st.session_state.language = "English"
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "backend_ok" not in st.session_state:
    st.session_state.backend_ok = check_backend()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px;">
        <div style="font-size:2.4rem">🌾</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:white;margin-top:4px">AgriGenAI</div>
        <div style="font-size:0.75rem;color:#a5d6a7;margin-top:2px">Farming Copilot</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Backend status
    if st.session_state.backend_ok:
        st.markdown('<div class="conn-online">🟢 Backend Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="conn-offline">🔴 Backend Offline</div>', unsafe_allow_html=True)
        st.caption("Run: `uvicorn app.main:app --reload --port 8000`")
    
    if st.button("🔄 Reconnect", key="reconnect"):
        st.session_state.backend_ok = check_backend()
        st.rerun()

    st.divider()
    st.markdown("**👤 Farmer Profile**")
    st.session_state.farmer_name = st.text_input(
        "Your Name", value=st.session_state.farmer_name,
        placeholder="e.g. Ramesh Patil", key="s_name"
    )
    new_loc = st.text_input(
        "Your Location", value=st.session_state.farmer_location,
        placeholder="e.g. Nashik, MH", key="s_loc"
    )
    if new_loc != st.session_state.farmer_location:
        st.session_state.farmer_location = new_loc
        st.session_state.weather_data = None

    st.session_state.farmer_crop = st.text_input(
        "Primary Crop", value=st.session_state.farmer_crop,
        placeholder="e.g. Wheat", key="s_crop"
    )

    st.divider()
    st.markdown("**🌐 Language**")
    lang_options = ["English", "हिन्दी (Hindi)", "मराठी (Marathi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "ಕನ್ನಡ (Kannada)", "ਪੰਜਾਬੀ (Punjabi)"]
    st.session_state.language = st.selectbox(
        "Respond in", lang_options,
        index=lang_options.index(st.session_state.language) if st.session_state.language in lang_options else 0,
        label_visibility="collapsed"
    )
    lang_hint = {
        "English": "en", "हिन्दी (Hindi)": "hi", "मराठी (Marathi)": "mr",
        "தமிழ் (Tamil)": "ta", "తెలుగు (Telugu)": "te",
        "ಕನ್ನಡ (Kannada)": "kn", "ਪੰਜਾਬੀ (Punjabi)": "pa"
    }
    st.caption(f"Language code: `{lang_hint.get(st.session_state.language, 'en')}`")

    st.divider()
    st.markdown("**📊 Session Stats**")
    total_calls = len(st.session_state.audit_log)
    blocked_calls = sum(1 for e in st.session_state.audit_log if e["status"] == "blocked")
    offline_calls = sum(1 for e in st.session_state.audit_log if e["source"] == "offline")
    st.metric("Total Queries", total_calls)
    col_a, col_b = st.columns(2)
    col_a.metric("Blocked", blocked_calls, delta=None)
    col_b.metric("Offline", offline_calls, delta=None)

    st.divider()
    if st.button("🗑️ Clear Session", key="clear_session"):
        for key in ["msgs", "audit_log", "weather_data"]:
            st.session_state.pop(key, None)
        st.rerun()

# ── HEADER ────────────────────────────────────────────────────────────────────
top_left, top_right = st.columns([3, 2])
with top_left:
    name_part = f", {st.session_state.farmer_name}!" if st.session_state.farmer_name else "!"
    st.markdown(f"""
    <div class="main-header">🌾 AgriGenAI{name_part}</div>
    <div class="main-subheader">Climate · Market · Crop Intelligence — for every farmer in India</div>
    """, unsafe_allow_html=True)

with top_right:
    # Load weather if needed
    if st.session_state.weather_data is None and st.session_state.farmer_location:
        try:
            wr = requests.get(f"{API}/weather", params={"location": st.session_state.farmer_location}, timeout=10)
            if wr.status_code == 200:
                st.session_state.weather_data = wr.json()
                audit("Weather Fetch", f"Location: {st.session_state.farmer_location}", source="online")
        except Exception:
            pass

    w = st.session_state.weather_data
    if w:
        days_html = "".join(
            f'<div style="text-align:center;min-width:38px">'
            f'<div style="font-size:10px;color:#78909c;font-weight:600">{d["day"]}</div>'
            f'<div style="font-size:18px">{d["icon"]}</div>'
            f'<div style="font-size:11px;font-weight:700;color:#37474f">{d["max"]}°</div>'
            f'<div style="font-size:10px;color:#b0bec5">{d["min"]}°</div>'
            f'</div>'
            for d in w["forecast"][:7]
        )
        alerts_html = ""
        if w.get("alerts"):
            alerts_html = f'<div style="font-size:11px;color:#e65100;margin-top:6px">⚠️ {w["alerts"][0]}</div>'
        st.markdown(
            f'<div class="weather-mini">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">'
            f'<span style="font-size:30px">{w.get("icon","🌤️")}</span>'
            f'<div>'
            f'<div style="font-family:DM Serif Display,serif;font-size:1.6rem;color:#1a237e;line-height:1">{w["temp"]}°C</div>'
            f'<div style="font-size:0.78rem;color:#455a64">{w["location"]} · {w["description"]}</div>'
            f'<div style="font-size:0.72rem;color:#78909c">💧{w["humidity"]}% · 💨{w["wind"]}km/h · UV {w.get("uv_index","–")}</div>'
            f'</div></div>'
            f'<div style="display:flex;gap:8px;padding-top:4px;border-top:1px solid rgba(0,0,0,0.07)">{days_html}</div>'
            f'{alerts_html}</div>',
            unsafe_allow_html=True
        )
    else:
        st.info(f"⏳ Weather loading for {st.session_state.farmer_location}... (Backend must be running)")

st.divider()

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 Chat", "🌱 Crop Plan", "🐛 Pest Detection",
    "📈 Market", "🏛️ Schemes", "🌤️ Weather", "📋 Audit Log"
])

# ─────────────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────────────
with tab1:
    st.subheader("Ask AgriGenAI Anything")
    st.caption("Multi-lingual farming assistant — responds in your selected language")

    # Quick prompt chips
    st.markdown("**Quick Questions:**")
    chips = [
        f"Best crops for {st.session_state.farmer_location} this Kharif season",
        f"Current MSP for {st.session_state.farmer_crop}",
        "How to improve soil health organically",
        "Signs of nitrogen deficiency in crops",
        "PM-KISAN eligibility and how to apply",
        "Water saving techniques for dry regions",
    ]
    chips_html = "".join(f'<span class="chat-chip" onclick="void(0)" title="{c}">🌿 {c[:40]}{"..." if len(c)>40 else ""}</span>' for c in chips)
    st.markdown(f'<div style="margin-bottom:12px">{chips_html}</div>', unsafe_allow_html=True)
    st.caption("💡 Click a chip or type below. Copy a chip text to the chat input to use it.")

    # Chat history display
    chat_container = st.container()
    with chat_container:
        for m in st.session_state.msgs:
            with st.chat_message(m["role"]):
                if m.get("offline"):
                    st.caption("📴 Offline mode — local ICAR knowledge base")
                if m.get("blocked"):
                    st.warning(m["content"])
                else:
                    st.markdown(m["content"])

    # Voice input
    with st.expander("🎙️ Voice Input (WAV / MP3 / M4A)"):
        audio_col1, audio_col2 = st.columns([3, 1])
        with audio_col1:
            audio_file = st.file_uploader(
                "Upload audio file", type=["wav", "mp3", "m4a", "ogg"],
                key="voice_upload", label_visibility="collapsed"
            )
        with audio_col2:
            transcribe_btn = st.button("🎙️ Transcribe", key="transcribe_btn", type="primary")
        
        if audio_file and transcribe_btn:
            with st.spinner("Transcribing with Whisper Large V3..."):
                try:
                    r = requests.post(
                        f"{API}/voice/transcribe",
                        files={"file": (audio_file.name, audio_file.getvalue(), audio_file.type)},
                        timeout=60
                    )
                    result = r.json()
                    if result.get("success"):
                        detected_lang = result.get("language", "")
                        text = result["text"]
                        st.success(f"🎙️ Detected ({detected_lang}): **{text}**")
                        st.session_state["prefill_chat"] = text
                        audit("Voice Transcription", f"Language: {detected_lang} | Text: {text[:80]}", source="online")
                    else:
                        st.error(f"Transcription failed: {result.get('error','')}")
                        audit("Voice Transcription", f"Failed: {result.get('error','')}", source="error", status="error")
                except Exception as e:
                    st.error(f"Could not reach backend: {e}")

    prefill = st.session_state.pop("prefill_chat", "")
    lang_code = lang_hint.get(st.session_state.language, "en")
    
    user_input = st.chat_input("Type in English, Hindi, Marathi, or any language...") or (prefill if prefill else None)

    if user_input:
        # Append language hint if non-English
        message_with_lang = user_input
        if lang_code != "en":
            message_with_lang = f"{user_input}\n[Please respond in {st.session_state.language}]"

        st.session_state.msgs.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("AgriGenAI is thinking..."):
                    data = post("/chat", {"message": message_with_lang}, audit_label="Chat Query")
                if data:
                    if data.get("blocked"):
                        st.warning(data["reply"])
                    else:
                        if data.get("offline"):
                            st.caption("📴 Offline mode — local ICAR knowledge base")
                        st.markdown(data["reply"])
                    st.session_state.msgs.append({
                        "role": "assistant",
                        "content": data["reply"],
                        "offline": data.get("offline", False),
                        "blocked": data.get("blocked", False),
                    })

    if st.session_state.msgs:
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.msgs = []
            st.rerun()


# ─────────────────────────────────────────────────
# TAB 2 — CROP PLAN
# ─────────────────────────────────────────────────
with tab2:
    st.subheader("🌱 Smart Crop Planning")
    st.caption("Get AI-powered crop recommendations tailored to your soil, season, and location")

    c1, c2, c3 = st.columns(3)
    with c1:
        loc = st.text_input("📍 Location / District", value=st.session_state.farmer_location, placeholder="e.g. Nashik, Maharashtra")
        soil = st.selectbox("🪨 Soil Type", ["Black", "Red", "Alluvial", "Sandy", "Loamy", "Clay"])
    with c2:
        season = st.selectbox("📅 Season", ["Kharif (Jun-Oct)", "Rabi (Nov-Mar)", "Zaid (Mar-Jun)"])
        water = st.selectbox("💧 Water Availability", ["low", "moderate", "high"])
    with c3:
        prev = st.text_input("🌾 Previous Crop (optional)", value=st.session_state.farmer_crop, placeholder="e.g. Wheat")
        st.markdown("")

    with st.expander("🧪 Soil Test Data — optional but greatly improves accuracy"):
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            nitrogen = st.number_input("Nitrogen (N) kg/ha", min_value=0.0, max_value=500.0, value=0.0, step=1.0)
        with sc2:
            phosphorus = st.number_input("Phosphorus (P) kg/ha", min_value=0.0, max_value=200.0, value=0.0, step=1.0)
        with sc3:
            potassium = st.number_input("Potassium (K) kg/ha", min_value=0.0, max_value=500.0, value=0.0, step=1.0)
        with sc4:
            ph_val = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=0.0, step=0.1,
                                      help="Ideal range: 6.0–7.5 for most crops")
        
        # pH indicator
        if ph_val > 0:
            if ph_val < 5.0:
                st.error(f"⚠️ pH {ph_val} is very acidic — may cause nutrient lockout. Consider lime application.")
            elif ph_val > 8.5:
                st.error(f"⚠️ pH {ph_val} is very alkaline — restricted crop selection. Consider sulfur treatment.")
            elif 6.0 <= ph_val <= 7.5:
                st.success(f"✅ pH {ph_val} — Ideal range for most crops")
            else:
                st.warning(f"⚠️ pH {ph_val} — Marginally outside optimal range")

    plan_btn = st.button("🌱 Get Crop Recommendations", type="primary", key="crop_plan_btn")

    if plan_btn:
        if not loc:
            st.warning("Please enter your location.")
        else:
            npk = {"n": nitrogen, "p": phosphorus, "k": potassium} if any([nitrogen, phosphorus, potassium]) else None
            ph = ph_val if ph_val > 0 else None
            payload = {
                "location": loc, "soil_type": soil, "season": season,
                "water_availability": water, "previous_crop": prev or None,
                "npk": npk, "ph": ph
            }
            with st.spinner("🌍 Analyzing soil, weather, and conditions..."):
                data = post("/crop/plan", payload, audit_label="Crop Planning")

            if data:
                crops = [c if isinstance(c, str) else str(c) for c in data.get("recommended_crops", [])]

                # Recommended crops as visual badges
                st.markdown("### ✅ Recommended Crops")
                badges = "".join(f'<span class="crop-badge">🌿 {crop}</span>' for crop in crops)
                st.markdown(f'<div style="margin:8px 0 16px">{badges}</div>', unsafe_allow_html=True)

                # Warnings
                if data.get("warnings"):
                    for w_msg in data["warnings"]:
                        st.warning(f"⚠️ {w_msg}")

                # Details in 3 columns
                d1, d2, d3 = st.columns(3)
                with d1:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🌤️ Weather Summary**")
                    st.write(data.get("weather_summary", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with d2:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🧪 Soil Advice**")
                    st.write(data.get("soil_advice", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with d3:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🌱 Planting Tips**")
                    st.write(data.get("planting_tips", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)

                # Metadata pills
                st.markdown(
                    f'<div style="margin-top:8px">'
                    f'<span class="stat-pill">📍 {loc}</span>'
                    f'<span class="stat-pill">🪨 {soil} soil</span>'
                    f'<span class="stat-pill">📅 {season}</span>'
                    f'<span class="stat-pill">💧 {water.capitalize()} water</span>'
                    f'{"<span class=stat-pill>🧪 NPK: " + str(nitrogen)+"/"+str(phosphorus)+"/"+str(potassium)+"</span>" if npk else ""}'
                    f'{"<span class=stat-pill>⚗️ pH: "+str(ph)+"</span>" if ph else ""}'
                    f'</div>',
                    unsafe_allow_html=True
                )


# ─────────────────────────────────────────────────
# TAB 3 — PEST DETECTION
# ─────────────────────────────────────────────────
with tab3:
    st.subheader("🐛 Crop Image Analysis")
    st.caption("Upload a clear photo of affected leaves or plants for AI-powered diagnosis using LLaMA 4 Scout vision")

    upload_col, info_col = st.columns([1, 1])
    with upload_col:
        img = st.file_uploader(
            "Upload crop photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if img:
            st.image(img, use_column_width=True, caption="Uploaded crop image")

    with info_col:
        st.markdown("""
        <div class="agri-card">
        <div style="font-family:DM Serif Display,serif;font-size:1.1rem;color:#1b5e20;margin-bottom:8px">📸 Tips for Better Results</div>
        <ul style="font-size:0.87rem;color:#555;line-height:1.8;margin:0;padding-left:16px">
            <li>Photograph affected leaves in natural daylight</li>
            <li>Include both upper and lower leaf surfaces</li>
            <li>Capture close-up of spots, discoloration, or insects</li>
            <li>Avoid blurry or dark images</li>
            <li>One plant/leaf per image for best accuracy</li>
        </ul>
        <div style="margin-top:12px;font-size:0.8rem;color:#888">
        🤖 Powered by Meta LLaMA 4 Scout 17B vision model
        </div>
        </div>
        """, unsafe_allow_html=True)

        if img:
            if st.button("🔍 Analyze for Pest & Disease", type="primary", key="pest_btn"):
                with st.spinner("🤖 AI vision model analyzing..."):
                    try:
                        r = requests.post(
                            f"{API}/pest/detect",
                            files={"file": (img.name, img.getvalue(), img.type)},
                            timeout=60
                        )
                        if r.status_code == 200:
                            d = r.json()
                            audit(
                                "Pest Detection",
                                f"Result: {'Healthy' if d.get('is_healthy') else d.get('pest_name','Unknown')} | Severity: {d.get('severity','–')} | Confidence: {round(float(d.get('confidence',0))*100)}%",
                                source="online",
                                metadata={"pest": d.get("pest_name"), "severity": d.get("severity"), "confidence": d.get("confidence")}
                            )
                            st.session_state["pest_result"] = d
                        else:
                            err = r.json().get('detail', r.text)
                            st.error(err)
                            audit("Pest Detection", f"Failed: {err}", source="error", status="error")
                    except Exception as e:
                        st.error(f"Backend error: {e}")

    # Display results
    if "pest_result" in st.session_state:
        d = st.session_state["pest_result"]
        st.divider()
        r1, r2 = st.columns([1, 2])
        with r1:
            if d.get("is_healthy"):
                st.markdown('<div style="text-align:center;padding:24px"><div style="font-size:3rem">✅</div><div style="font-family:DM Serif Display,serif;font-size:1.3rem;color:#2e7d32">Crop is Healthy!</div><div style="font-size:0.85rem;color:#666;margin-top:4px">No pest or disease detected</div></div>', unsafe_allow_html=True)
            else:
                sev = d.get("severity", "unknown")
                sev_map = {"mild": "sev-mild", "moderate": "sev-moderate", "severe": "sev-severe", "none": "sev-healthy"}
                conf_pct = round(float(d.get("confidence", 0)) * 100)
                st.markdown(f"""
                <div style="text-align:center;padding:16px">
                    <div style="font-size:2.5rem">🔬</div>
                    <div style="font-family:DM Serif Display,serif;font-size:1.2rem;color:#b71c1c;margin:8px 0">{d.get('pest_name','Unknown Pest')}</div>
                    <span class="severity-badge {sev_map.get(sev,'')}">{sev.upper()} Severity</span>
                    <div style="margin-top:10px">
                        <div style="font-size:0.8rem;color:#888;margin-bottom:4px">AI Confidence</div>
                        <div style="background:#eee;border-radius:8px;height:8px">
                            <div style="background:{"#f44336" if conf_pct<60 else "#ff9800" if conf_pct<80 else "#4caf50"};width:{conf_pct}%;height:8px;border-radius:8px"></div>
                        </div>
                        <div style="font-size:0.85rem;font-weight:600;color:#333;margin-top:4px">{conf_pct}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with r2:
            if not d.get("is_healthy"):
                st.markdown("**💊 Recommended Treatment**")
                st.markdown(d.get("treatment", "—"))
                if d.get("prevention"):
                    st.markdown("**🛡️ Prevention**")
                    st.markdown(d.get("prevention", "—"))
                if d.get("severity") in ["moderate", "severe"]:
                    st.warning("⚠️ **Safety:** Always wear protective gear when applying chemicals. Read label instructions carefully. Consult your local agriculture officer for approved pesticides.")


# ─────────────────────────────────────────────────
# TAB 4 — MARKET
# ─────────────────────────────────────────────────
with tab4:
    st.subheader("📈 Market Price Intelligence")
    st.caption("AI-powered price forecast + MSP comparison")

    m1, m2, m3 = st.columns([2, 2, 1])
    with m1:
        crop_name = st.text_input("🌾 Crop", value=st.session_state.farmer_crop, placeholder="e.g. Wheat, Rice, Cotton")
    with m2:
        mandi = st.text_input("🏪 Mandi / Location", value=st.session_state.farmer_location, placeholder="e.g. Pune, Nashik")
    with m3:
        st.markdown("")
        st.markdown("")
        forecast_btn = st.button("📊 Get Forecast", type="primary", key="market_btn")

    if forecast_btn:
        if not crop_name or not mandi:
            st.warning("Enter both crop name and mandi location.")
        else:
            with st.spinner("📡 Fetching market intelligence..."):
                data = post("/market/forecast", {"crop": crop_name, "location": mandi}, audit_label="Market Forecast")
            if data:
                st.session_state["market_result"] = data
                st.session_state["market_crop"] = crop_name

    if "market_result" in st.session_state:
        data = st.session_state["market_result"]
        crop_label = st.session_state.get("market_crop", "Crop")
        
        # Price cards
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(f"""
            <div class="price-card">
                <div class="price-label">Current Price</div>
                <div class="price-value">₹{data.get('current_price_per_kg', '–')}</div>
                <div class="price-unit">per kg</div>
            </div>""", unsafe_allow_html=True)
        with p2:
            p7 = data.get('predicted_price_7d', '–')
            curr = data.get('current_price_per_kg', 0)
            delta_7 = f"+₹{round(float(p7)-float(curr),2)}" if curr and p7 != '–' else ""
            st.markdown(f"""
            <div class="price-card">
                <div class="price-label">7-Day Forecast</div>
                <div class="price-value">₹{p7}</div>
                <div class="price-unit">per kg &nbsp; <span style="color:{'#2e7d32' if '+' in delta_7 else '#c62828'}">{delta_7}</span></div>
            </div>""", unsafe_allow_html=True)
        with p3:
            p30 = data.get('predicted_price_30d', '–')
            delta_30 = f"+₹{round(float(p30)-float(curr),2)}" if curr and p30 != '–' else ""
            st.markdown(f"""
            <div class="price-card">
                <div class="price-label">30-Day Forecast</div>
                <div class="price-value">₹{p30}</div>
                <div class="price-unit">per kg &nbsp; <span style="color:{'#2e7d32' if '+' in delta_30 else '#c62828'}">{delta_30}</span></div>
            </div>""", unsafe_allow_html=True)

        # Trend + sell window
        trend = data.get("trend", "stable")
        trend_icon = "📈" if trend == "rising" else "📉" if trend == "falling" else "➡️"
        trend_color = "#2e7d32" if trend == "rising" else "#c62828" if trend == "falling" else "#e65100"
        sell_window = data.get("best_sell_window", "—")

        st.markdown(f"""
        <div class="agri-card" style="margin-top:16px;display:flex;gap:24px;align-items:center;flex-wrap:wrap">
            <div>
                <div style="font-size:0.78rem;color:#888;font-weight:600">PRICE TREND</div>
                <div style="font-size:1.2rem;font-weight:700;color:{trend_color}">{trend_icon} {trend.capitalize()}</div>
            </div>
            <div style="width:1px;background:#e0e0e0;height:40px"></div>
            <div>
                <div style="font-size:0.78rem;color:#888;font-weight:600">BEST SELL WINDOW</div>
                <div style="font-size:1.05rem;font-weight:600;color:#1b5e20">⏰ {sell_window}</div>
            </div>
            <div style="width:1px;background:#e0e0e0;height:40px"></div>
            <div>
                <div style="font-size:0.78rem;color:#888;font-weight:600">CROP</div>
                <div style="font-size:1.05rem;font-weight:600;color:#33691e">🌾 {crop_label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if data.get("price_factors"):
            with st.expander("💡 Why these prices? (AI Analysis)"):
                st.markdown(data["price_factors"])


# ─────────────────────────────────────────────────
# TAB 5 — SCHEMES
# ─────────────────────────────────────────────────
with tab5:
    st.subheader("🏛️ Government Scheme Finder")
    st.caption("Discover central and state government schemes tailored to your profile")

    sq1, sq2 = st.columns([3, 1])
    with sq1:
        query = st.text_input("🔍 What are you looking for?", placeholder="e.g. crop insurance, loan waiver, organic farming subsidy")
    with sq2:
        st.markdown("")
        cat = st.selectbox("Farmer Category", ["small", "marginal", "large"])
    
    sc1, sc2 = st.columns(2)
    with sc1:
        state = st.text_input("State", value="Maharashtra", placeholder="e.g. Maharashtra")
    with sc2:
        s_crop = st.text_input("Crop", value=st.session_state.farmer_crop, placeholder="e.g. Rice")

    if st.button("🔍 Find Schemes", type="primary", key="schemes_btn"):
        if not query:
            st.warning("Please enter what you are looking for.")
        else:
            with st.spinner("Searching government scheme database..."):
                data = post("/schemes/search", {
                    "query": query, "state": state or None,
                    "crop": s_crop or None, "farmer_category": cat
                }, audit_label="Scheme Search")
            if data:
                st.session_state["schemes_result"] = data

    if "schemes_result" in st.session_state:
        data = st.session_state["schemes_result"]
        if data.get("summary"):
            st.markdown(f'<div class="agri-card">{data["summary"]}</div>', unsafe_allow_html=True)
        
        schemes = data.get("schemes", [])
        if schemes:
            st.markdown(f"**Found {len(schemes)} relevant scheme(s):**")
            for s in schemes:
                with st.expander(f"📋 {s['name']} — {s.get('full_name', '')}"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**What you get:** {s.get('benefit', '—')}")
                        st.markdown(f"**How to apply:** {s.get('how_to_apply', '—')}")
                    with col_b:
                        st.markdown(f"**Ministry:** {s.get('ministry', '—')}")
                        if s.get("deadline"):
                            st.markdown(f"**Deadline:** {s['deadline']}")
        else:
            st.info("No matching schemes found. Try a broader search query.")


# ─────────────────────────────────────────────────
# TAB 6 — WEATHER
# ─────────────────────────────────────────────────
with tab6:
    st.subheader("🌤️ Detailed Weather Report")

    w = st.session_state.get("weather_data")
    if not w:
        wloc = st.text_input("Enter location", value=st.session_state.farmer_location, key="weather_loc_input")
        if st.button("🔍 Load Weather", type="primary"):
            with st.spinner("Fetching weather..."):
                try:
                    wr = requests.get(f"{API}/weather", params={"location": wloc}, timeout=10)
                    if wr.status_code == 200:
                        st.session_state.weather_data = wr.json()
                        st.session_state.farmer_location = wloc
                        audit("Weather Fetch", f"Location: {wloc}", source="online")
                        st.rerun()
                except Exception as e:
                    st.error(f"Weather fetch failed: {e}")
    else:
        # Alerts
        if w.get("alerts"):
            for alert in w["alerts"]:
                st.warning(alert)

        # Current conditions
        st.markdown("#### ☀️ Current Conditions")
        mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
        mc1.metric("🌡️ Temp", f"{w['temp']}°C", f"Feels {w.get('feels_like', w['temp'])}°C")
        mc2.metric("💧 Humidity", f"{w['humidity']}%")
        mc3.metric("💨 Wind", f"{w['wind']} km/h")
        mc4.metric("☀️ UV Index", w.get('uv_index', '–'))
        mc5.metric("🌧️ Rain Now", f"{w.get('rain_now', 0)} mm")
        mc6.metric("📊 Pressure", f"{w.get('pressure', '–')} hPa")

        st.divider()
        st.markdown("#### 📅 10-Day Forecast")
        
        for day in w["forecast"]:
            rain_prob = day.get("rain_prob", 0)
            uv = day.get("uv", 0)
            rain_color = "#c62828" if rain_prob >= 70 else "#e65100" if rain_prob >= 40 else "#2e7d32"
            uv_color = "#c62828" if uv >= 9 else "#e65100" if uv >= 6 else "#2e7d32"
            farming_tip = ""
            if rain_prob >= 70:
                farming_tip = "🚫 Avoid spraying"
            elif rain_prob <= 20 and uv <= 6:
                farming_tip = "✅ Good for spraying"
            
            st.markdown(
                f'<div style="display:flex;align-items:center;background:white;border-radius:12px;padding:10px 16px;margin-bottom:6px;gap:12px;flex-wrap:wrap;box-shadow:0 1px 4px rgba(0,0,0,0.05);border:1px solid #f0ebe0">'
                f'<div style="min-width:90px;font-weight:600;font-size:0.88rem">{day["day"]} <span style="color:#aaa;font-size:11px">{day.get("date","")}</span></div>'
                f'<div style="font-size:22px">{day["icon"]}</div>'
                f'<div style="min-width:110px;font-size:0.82rem;color:#555">{day.get("desc","")}</div>'
                f'<div style="min-width:90px;font-size:0.85rem"><b>{day["max"]}°C</b> / {day["min"]}°C</div>'
                f'<div style="min-width:110px;font-size:0.82rem">🌧️ {day.get("rain_mm",0)}mm <span style="color:{rain_color};font-weight:700">{rain_prob}%</span></div>'
                f'<div style="min-width:90px;font-size:0.82rem">💨 {day.get("wind_max","–")} km/h</div>'
                f'<div style="min-width:60px;font-size:0.82rem">UV <span style="color:{uv_color};font-weight:700">{uv}</span></div>'
                f'<div style="font-size:0.78rem;color:#689f38;font-weight:500">{farming_tip}</div>'
                f'<div style="min-width:130px;font-size:0.75rem;color:#aaa">🌅{day.get("sunrise","")} 🌇{day.get("sunset","")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.divider()
        st.markdown("#### 🤖 AI Farming Advisory")
        if st.button("Generate Weather-Based Farming Advisory", type="primary", key="weather_advisory"):
            forecast_summary = ", ".join([
                f"{d['day']}: {d.get('desc','')} {d['max']}°/{d['min']}°C rain {d.get('rain_prob',0)}%"
                for d in w["forecast"][:5]
            ])
            advisory_prompt = (
                f"Location: {w['location']}. Current: {w['temp']}°C, {w['description']}, "
                f"humidity {w['humidity']}%, wind {w['wind']}km/h. "
                f"10-day forecast: {forecast_summary}. "
                f"Provide practical farming advisory: best days for sowing/spraying/harvesting, "
                f"weather risks, and crop protection tips."
            )
            with st.spinner("Generating AI advisory..."):
                r = requests.post(f"{API}/chat", json={"message": advisory_prompt}, timeout=120)
                if r.status_code == 200:
                    advisory = r.json().get("reply", "")
                    audit("Weather Advisory", f"Location: {w['location']} | 5-day summary generated", source="online")
                    st.markdown(advisory)


# ─────────────────────────────────────────────────
# TAB 7 — AUDIT LOG
# ─────────────────────────────────────────────────
with tab7:
    st.subheader("📋 Agent Decision Audit Log")
    st.caption("Full transparency trail — every AI agent action, data source, and guardrail decision is recorded here")

    log = st.session_state.get("audit_log", [])

    # Summary metrics
    a1, a2, a3, a4, a5 = st.columns(5)
    a1.metric("Total Decisions", len(log))
    a2.metric("Online Queries", sum(1 for e in log if e["source"] == "online"))
    a3.metric("Offline Queries", sum(1 for e in log if e["source"] == "offline"))
    a4.metric("Blocked (Guardrail)", sum(1 for e in log if e["status"] == "blocked"))
    a5.metric("Errors", sum(1 for e in log if e["status"] == "error"))

    # Filter controls
    st.divider()
    fcol1, fcol2, fcol3 = st.columns([2, 2, 1])
    with fcol1:
        filter_action = st.selectbox("Filter by Action", ["All"] + sorted(set(e["action"] for e in log)))
    with fcol2:
        filter_status = st.selectbox("Filter by Status", ["All", "ok", "blocked", "error", "offline"])
    with fcol3:
        st.markdown("")
        st.markdown("")
        if st.button("📥 Export JSON", key="export_audit"):
            audit_json = json.dumps(log, indent=2)
            st.download_button(
                "⬇️ Download audit.json",
                data=audit_json,
                file_name=f"agrigenaai_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    # Filtered entries
    filtered = [
        e for e in log
        if (filter_action == "All" or e["action"] == filter_action)
        and (filter_status == "All" or e["source"] == filter_status or e["status"] == filter_status)
    ]

    if not filtered:
        st.info("📭 No audit entries yet. Start using the app — every AI decision will be logged here automatically.")
        st.markdown("""
        <div class="agri-card" style="background:#f9fbe7">
        <div style="font-family:DM Serif Display,serif;font-size:1rem;color:#33691e;margin-bottom:8px">What gets logged?</div>
        <ul style="font-size:0.85rem;color:#555;line-height:2">
            <li>🌾 Chat queries — every message sent to the AI</li>
            <li>🌱 Crop planning requests — location, soil, season inputs</li>
            <li>🐛 Pest detection — image analysis results and confidence</li>
            <li>📈 Market forecasts — crop and location queried</li>
            <li>🏛️ Scheme searches — query and filters used</li>
            <li>🌤️ Weather fetches — location and data source</li>
            <li>🎙️ Voice transcriptions — language detected</li>
            <li>🚫 Guardrail blocks — what was blocked and why</li>
            <li>📴 Offline fallbacks — when local knowledge base was used</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(filtered)} entries** {'(filtered)' if len(filtered) < len(log) else ''}")
        for entry in filtered:
            status = entry["status"]
            source = entry["source"]
            card_class = "blocked" if status == "blocked" else "warning" if status == "error" else "offline" if source == "offline" else ""
            src_class = "blocked-src" if status == "blocked" else "offline-src" if source == "offline" else ""
            src_label = "🚫 BLOCKED" if status == "blocked" else "📴 OFFLINE" if source == "offline" else "⚠️ ERROR" if status == "error" else "🟢 ONLINE"
            
            meta_html = ""
            if entry.get("metadata"):
                meta_items = " · ".join(f"{k}: {v}" for k, v in entry["metadata"].items() if v is not None)
                if meta_items:
                    meta_html = f'<div style="font-size:0.75rem;color:#aaa;margin-top:4px">📎 {meta_items}</div>'

            st.markdown(
                f'<div class="audit-entry {card_class}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span class="audit-action">{entry["action"]}</span>'
                f'<span class="audit-time">{entry["date"]} {entry["ts"]}</span>'
                f'</div>'
                f'<div class="audit-detail">{entry["detail"]}</div>'
                f'{meta_html}'
                f'<span class="audit-source {src_class}">{src_label}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
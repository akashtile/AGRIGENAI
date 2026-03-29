"""
AgriGenAI — "Midnight Harvest" Premium Dark UI
Design system:
  Palette   : Deep forest #080f0a bg · Electric emerald #22c55e accent
              Amber #f59e0b harvest · Rose #f87171 danger · Cream #f0fdf4 text
  Typography: Syne (geometric display) + DM Sans (refined body)
  Cards     : Glass morphism on dark, emerald-tinted borders
  Components: Glowing metrics, pill chips, dark inputs, animated tabs
All bug fixes from v2 are preserved.
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

API = "http://localhost:8000"

st.set_page_config(
    page_title="AgriGenAI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — injected as global CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fonts ────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── CSS Variables ────────────────────────────────────────────── */
:root {
  --bg-base:       #070d08;
  --bg-surface:    #0d1a0f;
  --bg-raised:     #132116;
  --bg-glass:      rgba(34,197,94,0.05);
  --bg-glass-hover:rgba(34,197,94,0.09);

  --green-400:     #4ade80;
  --green-500:     #22c55e;
  --green-600:     #16a34a;
  --green-900:     #052e12;

  --amber-400:     #fbbf24;
  --amber-500:     #f59e0b;

  --rose-400:      #fb7185;
  --rose-500:      #f43f5e;

  --text-primary:  #ecfdf5;
  --text-secondary:#86efac;
  --text-muted:    #4ade8066;

  --border-subtle: rgba(34,197,94,0.15);
  --border-mid:    rgba(34,197,94,0.28);
  --border-bright: rgba(34,197,94,0.55);

  --shadow-glow:   0 0 24px rgba(34,197,94,0.12);
  --shadow-card:   0 4px 32px rgba(0,0,0,0.6);
  --radius-lg:     16px;
  --radius-md:     12px;
  --radius-sm:     8px;
  --radius-pill:   999px;
}

/* ── Base reset ───────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-primary) !important;
}

/* ── App background ───────────────────────────────────────────── */
.stApp {
  background: var(--bg-base) !important;
  /* Subtle dot-grid pattern for depth */
  background-image:
    radial-gradient(circle at 20% 20%, rgba(34,197,94,0.06) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(34,197,94,0.04) 0%, transparent 50%),
    radial-gradient(rgba(34,197,94,0.035) 1px, transparent 1px) !important;
  background-size: auto, auto, 28px 28px !important;
}

/* ── Main container ───────────────────────────────────────────── */
.main .block-container {
  padding: 1.6rem 2.4rem 3rem !important;
  max-width: 1380px !important;
}

/* ── Top header bar ───────────────────────────────────────────── */
[data-testid="stHeader"] {
  background: rgba(7,13,8,0.92) !important;
  backdrop-filter: blur(12px) !important;
  border-bottom: 1px solid var(--border-subtle) !important;
}

/* ── Divider ──────────────────────────────────────────────────── */
hr { border-color: var(--border-subtle) !important; margin: 1.2rem 0 !important; }

/* ══════════════════════════════════════════
   TYPOGRAPHY
══════════════════════════════════════════ */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  font-family: 'Syne', sans-serif !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.03em !important;
}
.stMarkdown h3 { font-size: 1.1rem !important; font-weight: 700 !important; }
.stMarkdown h4 { font-size: 1rem !important; font-weight: 600 !important; color: var(--green-400) !important; }
.stMarkdown p, .stMarkdown li { color: #c4e8d1 !important; line-height: 1.72 !important; }
.stMarkdown a { color: var(--green-400) !important; }
.stMarkdown strong { color: var(--text-primary) !important; }
/* ── Expander label ───────────────────────────────────────────── */
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
details summary p {
  font-size: 1.15rem !important;
  font-weight: 700 !important;
  color: var(--green-400) !important;
  font-family: 'Syne', sans-serif !important;
  letter-spacing: 0.01em !important;
}

.stMarkdown code {
  background: var(--bg-raised) !important; color: var(--green-400) !important;
  border: 1px solid var(--border-subtle) !important; border-radius: 5px !important;
  padding: 1px 6px !important; font-size: 0.87em !important;
}
.stMarkdown pre {
  background: var(--bg-raised) !important; border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important; padding: 14px 18px !important;
  color: #a3e4b8 !important;
}

/* Subheader */
[data-testid="stHeading"] {
  font-family: 'Syne', sans-serif !important;
  color: var(--text-primary) !important;
}

/* Caption */
.stMarkdown small, .stCaptionContainer p {
  color: #4ade8099 !important; font-size: 0.82rem !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-pill) !important;
  padding: 4px !important;
  gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-radius: var(--radius-pill) !important;
  color: #6ee7a0 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  padding: 7px 18px !important;
  transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
  background: var(--bg-glass-hover) !important;
  color: var(--green-400) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--green-600), var(--green-500)) !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 12px rgba(34,197,94,0.35) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ══════════════════════════════════════════
   INPUTS & FORM CONTROLS
══════════════════════════════════════════ */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  background: var(--bg-raised) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.93rem !important;
  padding: 10px 14px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--border-mid) !important;
  box-shadow: none !important;
  outline: none !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stFileUploader label, .stMultiSelect label {
  color: var(--text-secondary) !important;
  font-size: 0.84rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em !important;
  text-transform: uppercase !important;
}

/* Selectbox */
.stSelectbox [data-baseweb="select"] > div {
  background: var(--bg-raised) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within {
  border-color: var(--border-mid) !important;
  box-shadow: none !important;
}
[data-baseweb="popover"] {
  background: #1a2e1e !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--radius-md) !important;
}
[data-baseweb="menu"] { background: #1a2e1e !important; }
[role="option"] {
  color: #ffffff !important;
  background: #1a2e1e !important;
  font-size: 0.92rem !important;
}
[role="option"]:hover {
  background: rgba(34,197,94,0.2) !important;
  color: #ffffff !important;
}
[aria-selected="true"][role="option"] {
  background: rgba(34,197,94,0.25) !important;
  color: #4ade80 !important;
}

/* Multiselect */
.stMultiSelect [data-baseweb="tag"] {
  background: var(--green-900) !important;
  border: 1px solid var(--border-mid) !important;
  color: var(--green-400) !important;
  border-radius: var(--radius-pill) !important;
}

/* Number input spinners */
.stNumberInput button {
  background: var(--bg-raised) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--green-400) !important;
}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
  background: var(--bg-raised) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--green-400) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  padding: 8px 18px !important;
  transition: all 0.18s ease !important;
}
.stButton > button:hover {
  background: var(--bg-glass-hover) !important;
  border-color: var(--green-500) !important;
  color: #fff !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(34,197,94,0.2) !important;
}
/* Primary button */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--green-600), var(--green-500)) !important;
  border: none !important;
  color: #fff !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 2px 16px rgba(34,197,94,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, var(--green-500), #4ade80) !important;
  box-shadow: 0 4px 24px rgba(34,197,94,0.45) !important;
  transform: translateY(-2px) !important;
}
/* Download button */
.stDownloadButton > button {
  background: var(--bg-raised) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--green-400) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ══════════════════════════════════════════
   METRICS
══════════════════════════════════════════ */
[data-testid="stMetric"] {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  padding: 16px 18px !important;
}
[data-testid="stMetricLabel"] p {
  color: #6ee7a0 !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
  color: var(--text-primary) !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 1.6rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"] > div {
  font-size: 0.82rem !important;
  font-weight: 500 !important;
}

/* ══════════════════════════════════════════
   ALERT BOXES
══════════════════════════════════════════ */
/* ── Alerts / Notifications ───────────────────────────────────── */
/* success */
.stSuccess, div[data-testid="stNotification"].stSuccess,
[data-baseweb="notification"].stSuccess {
  background: rgba(34,197,94,0.15) !important;
  border: 1.5px solid #22c55e !important;
  border-radius: var(--radius-md) !important;
}
.stSuccess p, .stSuccess span, .stSuccess div {
  color: #4ade80 !important;
  font-weight: 600 !important;
}
/* info */
.stInfo, div[data-testid="stNotification"].stInfo,
[data-baseweb="notification"].stInfo {
  background: rgba(56,189,248,0.12) !important;
  border: 1.5px solid #38bdf8 !important;
  border-radius: var(--radius-md) !important;
}
.stInfo p, .stInfo span, .stInfo div {
  color: #7dd3fc !important;
  font-weight: 500 !important;
}
/* warning */
.stWarning, div[data-testid="stNotification"].stWarning,
[data-baseweb="notification"].stWarning {
  background: rgba(251,191,36,0.12) !important;
  border: 1.5px solid #fbbf24 !important;
  border-radius: var(--radius-md) !important;
}
.stWarning p, .stWarning span, .stWarning div {
  color: #fde68a !important;
  font-weight: 500 !important;
}
/* error */
.stError, div[data-testid="stNotification"].stError,
[data-baseweb="notification"].stError {
  background: rgba(244,63,94,0.13) !important;
  border: 1.5px solid #f43f5e !important;
  border-radius: var(--radius-md) !important;
}
.stError p, .stError span, .stError div {
  color: #fda4af !important;
  font-weight: 600 !important;
}
/* shared icon + text alignment */
.stAlert, .stSuccess, .stInfo, .stWarning, .stError {
  font-family: 'DM Sans', sans-serif !important;
  padding: 12px 16px !important;
}

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */
.streamlit-expanderHeader {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  transition: background 0.2s !important;
}
.streamlit-expanderHeader:hover {
  background: var(--bg-raised) !important;
  border-color: var(--border-mid) !important;
}
.streamlit-expanderContent {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-subtle) !important;
  border-top: none !important;
  border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
  padding: 16px !important;
}

/* ══════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════ */
[data-testid="stFileUploadDropzone"] {
  background: var(--bg-surface) !important;
  border: 2px dashed var(--border-mid) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-secondary) !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploadDropzone"]:hover {
  border-color: var(--green-500) !important;
  background: var(--bg-glass) !important;
}

/* ══════════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════════ */
[data-testid="stChatMessage"] {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-lg) !important;
  padding: 14px 18px !important;
  margin-bottom: 8px !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
  background: rgba(34,197,94,0.07) !important;
  border-color: var(--border-mid) !important;
}
[data-testid="stChatInput"] {
  background: var(--bg-surface) !important;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--radius-lg) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: #ffffff !important;
  caret-color: #ffffff !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(255,255,255,0.45) !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--green-500) !important;
  box-shadow: 0 0 0 3px rgba(34,197,94,0.12) !important;
}

/* ══════════════════════════════════════════
   SPINNER
══════════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--green-500) !important; }

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-mid); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--green-600); }

/* ══════════════════════════════════════════
   LINE CHART / BAR CHART
══════════════════════════════════════════ */
[data-testid="stVegaLiteChart"] { border-radius: var(--radius-md) !important; overflow: hidden !important; }

/* ══════════════════════════════════════════
   CHECKBOX
══════════════════════════════════════════ */
.stCheckbox label { color: var(--text-secondary) !important; font-size: 0.88rem !important; }
.stCheckbox [data-testid="stCheckbox"] {
  accent-color: var(--green-500) !important;
}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: var(--bg-surface) !important;
  border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] label { color: var(--text-secondary) !important; }
section[data-testid="stSidebar"] input {
  background: var(--bg-raised) !important;
  color: var(--text-primary) !important;
  border-color: var(--border-mid) !important;
}

/* ══════════════════════════════════════════
   CUSTOM COMPONENTS
══════════════════════════════════════════ */

/* Gradient header card */
.gh-card {
  background: linear-gradient(135deg, #091a0d 0%, #0d2a14 45%, #0a2010 100%);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 22px 28px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-card), var(--shadow-glow);
}
.gh-card::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 180px; height: 180px;
  background: radial-gradient(circle, rgba(34,197,94,0.12) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.gh-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.85rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.04em;
  line-height: 1.1;
}
.gh-title span { color: var(--green-400); }
.gh-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.84rem;
  color: #4ade8077;
  margin-top: 4px;
  letter-spacing: 0.04em;
}
.gh-badge {
  display: inline-block;
  background: rgba(34,197,94,0.12);
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-pill);
  color: var(--green-400);
  font-size: 0.73rem;
  font-weight: 600;
  padding: 2px 10px;
  margin-right: 6px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Weather glass card */
.wx-card {
  background: rgba(13,26,15,0.85);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-mid);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: var(--shadow-card);
}
.wx-temp {
  font-family: 'Syne', sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.04em;
  line-height: 1;
}
.wx-desc {
  font-size: 0.88rem;
  color: var(--text-secondary);
  margin-top: 2px;
}
.wx-meta {
  font-size: 0.8rem;
  color: #4ade8066;
  margin-top: 6px;
}
.wx-day {
  text-align: center;
  min-width: 38px;
  flex-shrink: 0;
}
.wx-day .d { font-size: 9.5px; color: #4ade8055; text-transform: uppercase; letter-spacing: .05em; }
.wx-day .i { font-size: 18px; line-height: 1.4; }
.wx-day .h { font-size: 12px; font-weight: 700; color: var(--text-primary); }
.wx-day .l { font-size: 10.5px; color: #4ade8055; }

/* Glass card — generic content card */
.g-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.4);
  margin-bottom: 12px;
}
.g-card-accent {
  border-left: 3px solid var(--green-500);
}

/* Crop chip */
.cc {
  display: inline-block;
  background: rgba(34,197,94,0.1);
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-pill);
  color: var(--green-400);
  font-size: 0.86rem;
  font-weight: 600;
  padding: 5px 16px;
  margin: 3px;
  letter-spacing: 0.01em;
}

/* Info tile (crop plan) */
.info-tile {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  height: 100%;
  min-height: 80px;
}
.info-tile-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--green-500);
  margin-bottom: 8px;
}
.info-tile-body {
  font-size: 0.88rem;
  color: #c4e8d1;
  line-height: 1.65;
}

/* Confidence bar */
.cbar-wrap {
  background: rgba(255,255,255,0.06);
  border-radius: 4px;
  height: 6px;
  margin: 8px 0 4px;
  overflow: hidden;
}
.cbar-fill { height: 100%; border-radius: 4px; }

/* Voice pending */
.vp-card {
  background: rgba(34,197,94,0.07);
  border: 1.5px solid var(--border-mid);
  border-radius: var(--radius-md);
  padding: 12px 18px;
  font-size: 0.92rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
}
.vp-card strong { color: var(--green-400); }

/* Offline badge */
.off-badge {
  display: inline-block;
  background: rgba(245,158,11,0.1);
  border: 1px solid rgba(245,158,11,0.3);
  border-radius: var(--radius-pill);
  color: var(--amber-400);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 10px;
  margin-bottom: 6px;
  letter-spacing: 0.04em;
}

/* Scheme card */
.sc-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 18px 22px;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}
.sc-card:hover { border-color: var(--border-mid); }
.sc-name {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--green-400);
  margin-bottom: 6px;
}
.sc-badge {
  display: inline-block;
  background: rgba(34,197,94,0.08);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  color: var(--text-secondary);
  font-size: 0.74rem;
  font-weight: 600;
  padding: 2px 9px;
  margin-right: 5px;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Audit entry */
.ae {
  background: var(--bg-surface);
  border-left: 3px solid var(--border-mid);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 11px 16px;
  margin-bottom: 7px;
  font-size: 0.85rem;
}
.ae-ok   { border-left-color: var(--green-500); }
.ae-err  { border-left-color: var(--rose-500); }
.ae-ep   { font-weight: 600; color: var(--green-400); font-family:'DM Sans',sans-serif; }
.ae-ts   { font-size: 0.74rem; color: #4ade8055; }
.ae-inp  { font-size: 0.78rem; color: #6ee7a066; font-family: monospace; margin-top:3px; }
.ae-guard{
  display: inline-block;
  background: rgba(245,158,11,0.1);
  border: 1px solid rgba(245,158,11,0.25);
  border-radius: var(--radius-pill);
  color: var(--amber-400);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 1px 8px;
  margin: 4px 4px 0 0;
}
.ae-err-msg { font-size: 0.8rem; color: var(--rose-400); margin-top: 4px; }

/* Status pill */
.pill-ok  { display:inline-block;background:rgba(34,197,94,0.18);border:1.5px solid #22c55e;border-radius:var(--radius-pill);color:#4ade80;font-size:0.75rem;font-weight:800;padding:2px 11px;letter-spacing:.06em; }
.pill-err { display:inline-block;background:rgba(244,63,94,0.18);border:1.5px solid #f43f5e;border-radius:var(--radius-pill);color:#f87171;font-size:0.75rem;font-weight:800;padding:2px 11px;letter-spacing:.06em; }

/* Stat chip */
.stat-row {
  display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px;
}
.stat-chip {
  background: var(--bg-raised);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  text-align: center;
  flex: 1; min-width: 80px;
}
.stat-chip .v { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:var(--text-primary); }
.stat-chip .l { font-size:0.72rem; color:#4ade8066; text-transform:uppercase; letter-spacing:.06em; margin-top:1px; }

/* Forecast row */
.fx-row {
  display: flex; align-items: center; gap: 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 11px 18px;
  margin-bottom: 5px;
  flex-wrap: wrap;
  transition: border-color .15s;
}
.fx-row:hover { border-color: var(--border-mid); }

/* Detection severity banner */
.sev-banner {
  border-left: 4px solid;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: 14px 18px;
  margin-bottom: 14px;
}
.sev-name { font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700; }
.sev-sub  { font-size:0.86rem; color:#a3a3a3; margin-top:3px; }

/* Pest history row */
.ph-row {
  display: flex; align-items: center; gap: 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 14px;
  margin-bottom: 5px;
  font-size: 0.85rem;
}

/* Section divider with label */
.sec-divider {
  display: flex; align-items: center; gap: 12px; margin: 20px 0 14px;
}
.sec-divider span {
  font-family:'Syne',sans-serif;
  font-size:0.88rem; font-weight:700;
  color:var(--green-400);
  text-transform:uppercase;
  letter-spacing:.08em;
  white-space:nowrap;
}
.sec-divider::before,.sec-divider::after {
  content:''; flex:1; height:1px; background:var(--border-subtle);
}

/* Dot status */
.dot { width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:5px;vertical-align:middle; }
.dot-on  { background:#22c55e; box-shadow:0 0 6px #22c55e88; }
.dot-off { background:#f59e0b; box-shadow:0 0 6px #f59e0b55; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ══════════════════════════════════════════════════════════════════
LANGUAGES = {
    "Auto-detect": None, "English": "en", "हिंदी (Hindi)": "hi",
    "मराठी (Marathi)": "mr", "தமிழ் (Tamil)": "ta", "తెలుగు (Telugu)": "te",
    "ਪੰਜਾਬੀ (Punjabi)": "pa", "ಕನ್ನಡ (Kannada)": "kn",
    "বাংলা (Bengali)": "bn", "ગુજરાતી (Gujarati)": "gu",
}
QUICK_QS = [
    "गेहूं में कौन सा खाद डालें?",
    "Best crop for black soil Nashik?",
    "PM-KISAN eligibility?",
    "When to sow Rabi crops?",
    "Cotton pest management?",
]
SEV_COLOR  = {"mild":"#f59e0b","moderate":"#f97316","severe":"#ef4444","none":"#22c55e"}
TREND_ICON = {"rising":"📈","falling":"📉","stable":"➡️"}

_DEFAULTS = {
    "msgs":[], "audit_log":[], "weather_location":"Nashik",
    "weather_data":None, "weather_error":None, "chat_lang_label":"Auto-detect",
    "pest_result":None, "pest_last_file":None, "voice_pending":None, "pest_history":[],
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _post(endpoint: str, payload: dict):
    ts = datetime.now().strftime("%H:%M:%S")
    try:
        r = requests.post(f"{API}{endpoint}", json=payload, timeout=120)
        if r.status_code != 200:
            err = r.json().get("detail", r.text)
            _audit(ts, endpoint, payload, error=err)
            st.error(f"API error: {err}")
            return None
        data = r.json()
        _audit(ts, endpoint, payload, response=data)
        return data
    except requests.exceptions.ConnectionError:
        msg = "Backend unreachable — is uvicorn running on port 8000?"
        _audit(ts, endpoint, payload, error=msg)
        st.error(f"⚠️ {msg}")
        return None
    except Exception as exc:
        _audit(ts, endpoint, payload, error=str(exc))
        st.error(str(exc))
        return None


def _audit(ts, ep, payload, response=None, error=None):
    guards = []
    if response:
        if response.get("blocked"):            guards.append("OFF-TOPIC BLOCK")
        for w in response.get("warnings", []): guards.append(f"WARN: {w}")
        if response.get("offline"):            guards.append("OFFLINE FALLBACK")
    st.session_state.audit_log.append({
        "time":ts, "endpoint":ep,
        "input":{k:v for k,v in payload.items() if v not in (None,"",{})},
        "status":"ERROR" if error else "OK", "error":error,
        "blocked":bool(response and response.get("blocked")),
        "offline":bool(response and response.get("offline")),
        "guardrails_triggered":guards,
    })


def _fetch_wx(loc):
    try:
        r = requests.get(f"{API}/weather", params={"location":loc}, timeout=10)
        return (r.json(), None) if r.status_code == 200 else (None, f"{r.status_code}: {r.text[:100]}")
    except requests.exceptions.ConnectionError:
        return None, "Backend unreachable — make sure uvicorn is running."
    except Exception as e:
        return None, str(e)


def _cbar(val, color="#22c55e"):
    pct = int(float(val)*100)
    return (
        f'<div class="cbar-wrap"><div class="cbar-fill" style="width:{pct}%;background:{color}"></div></div>'
        f'<div style="font-size:0.8rem;color:#6ee7a0;margin-bottom:6px">Confidence: <b style="color:{color}">{pct}%</b></div>'
    )


def _info_tile(label, body, icon=""):
    body = body.strip() if body and body.strip() else "<em style='color:#4ade8044'>No data — add more inputs for better advice.</em>"
    st.markdown(
        f'<div class="info-tile">'
        f'<div class="info-tile-label">{icon} {label}</div>'
        f'<div class="info-tile-body">{body}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _sec(label):
    st.markdown(f'<div class="sec-divider"><span>{label}</span></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════
col_brand, col_wx = st.columns([5, 3])

with col_brand:
    n_msgs   = len(st.session_state.msgs)
    n_audit  = len(st.session_state.audit_log)
    badges   = (
        f'<span class="gh-badge">🌐 Multilingual</span>'
        f'<span class="gh-badge">📴 Offline-ready</span>'
        f'<span class="gh-badge">🤖 LLaMA 3.3 70B</span>'
    )
    st.markdown(
        f'<div class="gh-card">'
        f'<div class="gh-title">🌾 <span>Agri</span>GenAI</div>'
        f'<div class="gh-sub">AI FARMING COPILOT · INDIA</div>'
        f'<div style="margin-top:12px">{badges}</div>'
        f'<div style="margin-top:14px;display:flex;gap:20px">'
        f'<div style="font-size:0.8rem;color:#4ade8066">💬 {n_msgs} messages this session</div>'
        f'<div style="font-size:0.8rem;color:#4ade8066">📋 {n_audit} audit entries</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

with col_wx:
    w_input = st.text_input(
        "Location",
        value=st.session_state.weather_location,
        placeholder="City for weather — e.g. Nashik",
        label_visibility="collapsed",
    )
    if w_input != st.session_state.weather_location:
        st.session_state.weather_location = w_input
        st.session_state.weather_data     = None
        st.session_state.weather_error    = None

    if st.session_state.weather_data is None and st.session_state.weather_location:
        with st.spinner(f"Loading weather for {st.session_state.weather_location}…"):
            wd, we = _fetch_wx(st.session_state.weather_location)
            st.session_state.weather_data  = wd
            st.session_state.weather_error = we

    w    = st.session_state.weather_data
    w_er = st.session_state.weather_error

    if w:
        days_html = "".join(
            f'<div class="wx-day">'
            f'<div class="d">{d["day"]}</div>'
            f'<div class="i">{d["icon"]}</div>'
            f'<div class="h">{d["max"]}°</div>'
            f'<div class="l">{d["min"]}°</div></div>'
            for d in w["forecast"][:7]
        )
        dot = '<span class="dot dot-on"></span>' if not w.get("offline") else '<span class="dot dot-off"></span>'
        st.markdown(
            f'<div class="wx-card">'
            f'<div style="font-size:11px;color:#4ade8066;font-weight:600;letter-spacing:.06em;text-transform:uppercase">'
            f'{dot}{w["location"]}</div>'
            f'<div style="display:flex;align-items:flex-end;gap:12px;margin:8px 0 4px">'
            f'<span style="font-size:2.4rem;line-height:1">{w.get("icon","🌤️")}</span>'
            f'<span class="wx-temp">{w["temp"]}°C</span>'
            f'<span class="wx-desc">{w["description"]}</span>'
            f'</div>'
            f'<div class="wx-meta">💧 {w["humidity"]}% &nbsp;·&nbsp; 💨 {w["wind"]} km/h &nbsp;·&nbsp; 🌡️ Feels {w.get("feels_like",w["temp"])}°C</div>'
            f'<div style="display:flex;gap:8px;margin-top:10px;overflow-x:auto;padding-bottom:2px">{days_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif w_er:
        st.error(f"⚠️ Weather unavailable: {w_er}")
    else:
        st.markdown(
            '<div class="wx-card" style="min-height:100px;display:flex;align-items:center;justify-content:center">'
            '<span style="color:#4ade8044;font-size:0.88rem">Enter a city name above</span></div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr style="margin:18px 0 12px">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 Chat", "🌱 Crop Plan", "🐛 Pest Detection",
    "📈 Market", "🏛️ Schemes", "🌤️ Weather", "📋 Audit Log",
])

# ─────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────
with tab1:
    st.subheader("Ask anything about farming")

    ctrl_l, ctrl_r = st.columns([4, 1])
    with ctrl_l:
        lang_label = st.selectbox(
            "Reply language",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state.chat_lang_label),
            key="lang_sel", label_visibility="collapsed",
        )
        st.session_state.chat_lang_label = lang_label
        sel_lang = LANGUAGES[lang_label]
    with ctrl_r:
        if st.button("🗑️ Clear history", key="clear_chat", use_container_width=True):
            st.session_state.msgs = []
            st.rerun()

    # Quick chips
    _sec("Quick Questions")
    qcols = st.columns(len(QUICK_QS))
    for i, q in enumerate(QUICK_QS):
        with qcols[i]:
            label = q if len(q) <= 24 else q[:22] + "…"
            if st.button(label, key=f"qchip_{i}", use_container_width=True, help=q):
                st.session_state.voice_pending = q

    # Voice
    with st.expander("🎙️ Voice Input"):
        af = st.file_uploader("Upload audio WAV / MP3 / M4A", type=["wav","mp3","m4a","ogg"], key="vu")
        if af and st.button("Transcribe with Whisper", key="tb"):
            with st.spinner("Transcribing…"):
                rsp = requests.post(
                    f"{API}/voice/transcribe",
                    files={"file":(af.name, af.getvalue(), af.type)}, timeout=60,
                )
            if rsp.status_code == 200:
                res = rsp.json()
                if res.get("success"):
                    st.success(f"[{res.get('language','').upper()}] {res['text']}")
                    st.session_state.voice_pending = res["text"]
                    _audit(datetime.now().strftime("%H:%M:%S"), "/voice/transcribe", {"file":af.name}, response=res)
                    st.rerun()
                else:
                    st.error(f"Failed: {res.get('error','')}")
            else:
                st.error("Transcription failed — check backend")

    # Pending message card
    user_to_send = None
    if st.session_state.voice_pending:
        pt = st.session_state.voice_pending
        st.markdown(
            f'<div class="vp-card">📝 <strong>Ready to send:</strong> {pt}</div>',
            unsafe_allow_html=True,
        )
        sc, xc = st.columns([3,1])
        with sc:
            if st.button("▶ Send", type="primary", use_container_width=True, key="sp"):
                user_to_send = pt
                st.session_state.voice_pending = None
        with xc:
            if st.button("✕", use_container_width=True, key="cp"):
                st.session_state.voice_pending = None
                st.rerun()

    # Chat history container
    chat_box = st.container(height=390)
    with chat_box:
        for m in st.session_state.msgs:
            with st.chat_message(m["role"]):
                if m.get("offline"):
                    st.markdown('<span class="off-badge">📴 OFFLINE · ICAR KB</span>', unsafe_allow_html=True)
                st.markdown(m["content"])
                if m.get("suggestions"):
                    st.caption("💡 " + " · ".join(m["suggestions"]))

    typed = st.chat_input("Ask in English, Hindi, Marathi, Tamil…")
    if typed:
        user_to_send = typed

    if user_to_send:
        msg = user_to_send
        payload = {"message": msg}
        if sel_lang:
            payload["language"] = sel_lang

        st.session_state.msgs.append({"role":"user","content":msg})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(msg)
        with st.spinner("Thinking…"):
            data = _post("/chat", payload)
        if data:
            reply = data.get("reply","")
            with chat_box:
                with st.chat_message("assistant"):
                    if data.get("offline"):
                        st.markdown('<span class="off-badge">📴 OFFLINE · ICAR KB</span>', unsafe_allow_html=True)
                    if data.get("blocked"):
                        st.warning(reply)
                    else:
                        st.markdown(reply)
                    if data.get("suggestions"):
                        st.caption("💡 " + " · ".join(data["suggestions"]))
            st.session_state.msgs.append({
                "role":"assistant","content":reply,
                "offline":data.get("offline",False),
                "suggestions":data.get("suggestions",[]),
            })
        st.rerun()

# ─────────────────────────────────────────
# TAB 2 — CROP PLAN
# ─────────────────────────────────────────
with tab2:
    st.subheader("Smart Crop Recommendations")
    st.caption("Soil · Weather · Season · Water — all combined into one AI crop plan")

    crop_tab1, crop_tab2 = st.tabs(["🌱 Season Crop Plan", "📅 Full Year Farming Plan"])

    with crop_tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            loc    = st.text_input("📍 Location / District", placeholder="e.g. Nashik, Maharashtra")
            soil   = st.selectbox("🪨 Soil Type", ["Black","Red","Alluvial","Sandy","Loamy","Clay"])
        with c2:
            season = st.selectbox("🗓️ Season", ["Kharif (Jun-Oct)","Rabi (Nov-Mar)","Zaid (Mar-Jun)"])
            water  = st.selectbox("💧 Water Availability", ["low","moderate","high"])
        with c3:
            prev   = st.text_input("🔄 Previous Crop", placeholder="e.g. Wheat (optional)")
            area   = st.number_input("🌾 Farm Area (acres)", min_value=0.5, max_value=500.0, value=2.0, step=0.5)

        with st.expander("🧪 Soil Test Data — significantly improves recommendations"):
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1: nitrogen   = st.number_input("N (kg/ha)",  0.0, 500.0, 0.0, 1.0)
            with sc2: phosphorus = st.number_input("P (kg/ha)",  0.0, 200.0, 0.0, 1.0)
            with sc3: potassium  = st.number_input("K (kg/ha)",  0.0, 500.0, 0.0, 1.0)
            with sc4: ph_val     = st.number_input("pH",         0.0,  14.0, 0.0, 0.1)

        if st.button("🌱 Generate Crop Plan", type="primary", use_container_width=True):
            if not loc:
                st.warning("Please enter your location.")
            else:
                npk = {"n":nitrogen,"p":phosphorus,"k":potassium} if any([nitrogen,phosphorus,potassium]) else None
                ph  = ph_val if ph_val > 0 else None
                with st.spinner("Analyzing soil · weather · season with AI…"):
                    data = _post("/crop/plan", {
                        "location":loc,"soil_type":soil,"season":season,
                        "water_availability":water,"previous_crop":prev or None,
                        "npk":npk,"ph":ph,
                    })
                if data:
                    crops = [c if isinstance(c,str) else str(c) for c in data.get("recommended_crops",[])]

                    _sec("Recommended Crops")
                    chips = "".join(f'<span class="cc">🌿 {c}</span>' for c in crops)
                    st.markdown(chips + "<br>", unsafe_allow_html=True)

                    for wm in data.get("warnings",[]):
                        st.warning(f"⚠️ {wm}")

                    _sec("Field Intelligence")
                    p1, p2, p3 = st.columns(3)
                    with p1:
                        _info_tile("Weather Summary", data.get("weather_summary",""), "🌤️")
                    with p2:
                        sa = data.get("soil_advice","")
                        _info_tile("Soil Advice", sa if sa else
                            "No soil test data provided — add NPK/pH for personalised advice.", "🧪")
                    with p3:
                        _info_tile(
                            f"Area · {area} acres",
                            f"Scale seed and input quantities for {area} acres of {soil.lower()} soil. "
                            f"Refer to your state KVK guidelines for crop-specific rates.", "📐"
                        )

                    _sec("Planting Schedule & Tips")
                    tips = data.get("planting_tips","")
                    if tips:
                        st.markdown(tips)
                    else:
                        st.info("No tips returned — try adding location/soil detail.")

                    with st.expander("📄 Export Crop Plan"):
                        txt = (
                            f"AgriGenAI Crop Plan — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"{'='*54}\n"
                            f"Location   : {loc}\nSeason     : {season}\n"
                            f"Soil       : {soil}  |  Water: {water}\n"
                            f"Prev Crop  : {prev or 'None'}\nArea       : {area} acres\n\n"
                            f"Recommended Crops: {', '.join(crops)}\n\n"
                            f"Weather Summary:\n{data.get('weather_summary','')}\n\n"
                            f"Soil Advice:\n{data.get('soil_advice','')}\n\n"
                            f"Planting Tips:\n{data.get('planting_tips','')}\n\n"
                            f"Warnings: {'; '.join(data.get('warnings',[])) or 'None'}\n"
                        )
                        st.code(txt, language=None)
                        st.download_button("⬇️ Download .txt", txt,
                            file_name=f"crop_plan_{loc.replace(' ','_')}.txt", mime="text/plain")

    # ── Full Year Farming Plan ──────────────────────────────────────────────
    with crop_tab2:
        st.caption("AI-generated 12-month farming calendar tailored to your location, soil & water")

        fy1, fy2, fy3 = st.columns(3)
        with fy1:
            fy_loc  = st.text_input("📍 Location / District", placeholder="e.g. Pune, Maharashtra", key="fy_loc")
            fy_soil = st.selectbox("🪨 Soil Type", ["Black","Red","Alluvial","Sandy","Loamy","Clay"], key="fy_soil")
        with fy2:
            fy_water = st.selectbox("💧 Water Availability", ["low","moderate","high"], key="fy_water")
            fy_area  = st.number_input("🌾 Farm Area (acres)", min_value=0.5, max_value=500.0, value=2.0, step=0.5, key="fy_area")
        with fy3:
            with st.expander("🧪 Soil Test (optional)"):
                fy_n  = st.number_input("N (kg/ha)", 0.0, 500.0, 0.0, 1.0, key="fy_n")
                fy_p  = st.number_input("P (kg/ha)", 0.0, 200.0, 0.0, 1.0, key="fy_p")
                fy_k  = st.number_input("K (kg/ha)", 0.0, 500.0, 0.0, 1.0, key="fy_k")
                fy_ph = st.number_input("pH",        0.0,  14.0, 0.0, 0.1, key="fy_ph")

        if st.button("📅 Generate Full Year Plan", type="primary", use_container_width=True, key="fy_btn"):
            if not fy_loc:
                st.warning("Please enter your location.")
            else:
                fy_npk = {"n":fy_n,"p":fy_p,"k":fy_k} if any([fy_n,fy_p,fy_k]) else None
                fy_ph_val = fy_ph if fy_ph > 0 else None
                with st.spinner("Building your 12-month farming calendar with AI…"):
                    fy_data = _post("/crop/fullyear", {
                        "location": fy_loc, "soil_type": fy_soil,
                        "water_availability": fy_water, "farm_area": fy_area,
                        "npk": fy_npk, "ph": fy_ph_val,
                    })
                if fy_data:
                    if fy_data.get("summary"):
                        st.info(f"📋 {fy_data['summary']}")

                    key_crops = fy_data.get("key_crops", [])
                    if key_crops:
                        _sec("Key Crops This Year")
                        chips = "".join(f'<span class="cc">🌿 {c}</span>' for c in key_crops)
                        st.markdown(chips + "<br>", unsafe_allow_html=True)

                    _sec("12-Month Farming Calendar")

                    SEASON_COLOR = {
                        "Kharif":     "#22c55e",
                        "Rabi":       "#60a5fa",
                        "Zaid":       "#fbbf24",
                        "Off-season": "#a78bfa",
                    }

                    months = fy_data.get("months", [])
                    # render in 3 rows of 4 months
                    for row_start in range(0, 12, 4):
                        row_months = months[row_start:row_start+4]
                        cols = st.columns(4)
                        for col, m in zip(cols, row_months):
                            season_name = m.get("season","")
                            sc = SEASON_COLOR.get(season_name, "#4ade80")
                            crops_list  = ", ".join(m.get("crops",[])) or "—"
                            acts        = m.get("activities", [])
                            tip         = m.get("tips","")
                            acts_html   = "".join(
                                f'<div style="font-size:0.78rem;color:#c4e8d1;padding:2px 0;'
                                f'border-left:2px solid {sc}33;padding-left:6px;margin-bottom:3px">{a}</div>'
                                for a in acts
                            )
                            with col:
                                st.markdown(
                                    f'<div class="g-card" style="border-top:3px solid {sc};min-height:220px">'
                                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                                    f'<span style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#fff">{m.get("month","")}</span>'
                                    f'<span style="font-size:0.68rem;font-weight:700;color:{sc};background:{sc}22;'
                                    f'border-radius:999px;padding:2px 8px;border:1px solid {sc}44">{season_name}</span>'
                                    f'</div>'
                                    f'<div style="font-size:0.78rem;color:#4ade80;font-weight:600;margin-bottom:4px">🌿 Crops</div>'
                                    f'<div style="font-size:0.82rem;color:#ecfdf5;margin-bottom:10px">{crops_list}</div>'
                                    f'<div style="font-size:0.78rem;color:#4ade80;font-weight:600;margin-bottom:4px">📌 Activities</div>'
                                    f'{acts_html}'
                                    f'{"<div style=margin-top:8px;font-size:0.75rem;color:#4ade8077;font-style:italic>" + tip + "</div>" if tip else ""}'
                                    f'</div>',
                                    unsafe_allow_html=True,
                                )

                    # Export
                    with st.expander("📄 Export Full Year Plan"):
                        lines = [
                            f"AgriGenAI Full Year Farming Plan — {datetime.now().strftime('%Y-%m-%d')}",
                            f"{'='*54}",
                            f"Location : {fy_loc}  |  Soil: {fy_soil}  |  Water: {fy_water}  |  Area: {fy_area} acres",
                            f"Key Crops: {', '.join(key_crops)}",
                            f"Summary  : {fy_data.get('summary','')}",
                            "",
                        ]
                        for m in months:
                            lines.append(f"── {m.get('month','')} ({m.get('season','')}) ──")
                            lines.append(f"  Crops     : {', '.join(m.get('crops',[]))}")
                            lines.append(f"  Activities: {' | '.join(m.get('activities',[]))}")
                            if m.get("tips"):
                                lines.append(f"  Tip       : {m['tips']}")
                            lines.append("")
                        export_txt = "\n".join(lines)
                        st.code(export_txt, language=None)
                        st.download_button("⬇️ Download .txt", export_txt,
                            file_name=f"fullyear_plan_{fy_loc.replace(' ','_')}.txt", mime="text/plain")

# ─────────────────────────────────────────
# TAB 3 — PEST DETECTION
# ─────────────────────────────────────────
with tab3:
    st.subheader("AI Pest & Disease Detection")
    st.caption("Llama 4 Scout 17B vision model · Upload any crop photo for instant diagnosis")

    ic, rc = st.columns([1, 2])
    with ic:
        img = st.file_uploader("📸 Upload crop photo", type=["jpg","jpeg","png"])
        if img is not None:
            if img.name != st.session_state.pest_last_file:
                st.session_state.pest_result    = None
                st.session_state.pest_last_file = img.name
            st.image(img, use_column_width=True, caption=img.name)
        else:
            st.session_state.pest_result    = None
            st.session_state.pest_last_file = None

    with rc:
        if img is None:
            st.markdown(
                '<div class="info-tile" style="min-height:180px;display:flex;align-items:center;justify-content:center">'
                '<span style="color:#4ade8044;font-size:0.92rem">Upload a crop photo on the left →</span>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button("🔬 Analyze Crop", type="primary", use_container_width=True):
                with st.spinner("Running vision model…"):
                    rsp = requests.post(f"{API}/pest/detect",
                        files={"file":(img.name, img.getvalue(), img.type)}, timeout=60)
                ts = datetime.now().strftime("%H:%M:%S")
                if rsp.status_code == 200:
                    d = rsp.json()
                    st.session_state.pest_result = d
                    _audit(ts, "/pest/detect", {"file":img.name}, response=d)
                    st.session_state.pest_history.append({
                        "time":ts,"file":img.name,
                        "pest":d.get("pest_name","Unknown"),
                        "severity":d.get("severity","none"),
                        "healthy":d.get("is_healthy",False),
                        "confidence":d.get("confidence",0),
                    })
                else:
                    st.error(rsp.json().get("detail", rsp.text))

            d = st.session_state.pest_result
            if d is not None:
                if d.get("is_healthy"):
                    st.success("✅ Crop is healthy — no pest or disease detected.")
                    st.balloons()
                else:
                    sev   = d.get("severity","none")
                    sc    = SEV_COLOR.get(sev,"#888")
                    pname = d.get("pest_name","Unknown")
                    st.markdown(
                        f'<div class="sev-banner" style="background:rgba(0,0,0,0.3);border-color:{sc}">'
                        f'<div class="sev-name" style="color:{sc}">⚠️ {pname}</div>'
                        f'<div class="sev-sub">Severity: <span style="color:{sc};font-weight:600">{sev.capitalize()}</span></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(_cbar(d.get("confidence",0), sc), unsafe_allow_html=True)

                _sec("Treatment")
                st.markdown(d.get("treatment") or "_No treatment info returned._")
                if d.get("prevention"):
                    _sec("Prevention")
                    st.markdown(d["prevention"])
                if d.get("severity") in ["moderate","severe"]:
                    st.warning("🧤 Use protective gear. Follow label dosage exactly when applying chemicals.")

    if st.session_state.pest_history:
        _sec("Detection History · This Session")
        for e in reversed(st.session_state.pest_history[-5:]):
            sc2    = SEV_COLOR.get(e["severity"],"#888")
            status = "✅ Healthy" if e["healthy"] else f"⚠️ {e['pest']} · {e['severity']}"
            conf   = int(float(e["confidence"])*100)
            st.markdown(
                f'<div class="ph-row">'
                f'<span style="font-size:0.74rem;color:#4ade8044;min-width:56px">{e["time"]}</span>'
                f'<span style="flex:1;color:#86efac">{e["file"]}</span>'
                f'<span style="font-weight:600;color:{sc2}">{status}</span>'
                f'<span style="font-size:0.8rem;color:#4ade8055">{conf}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────
# TAB 4 — MARKET
# ─────────────────────────────────────────
with tab4:
    st.subheader("Market Price Forecast")
    st.caption("AI-powered price predictions + MSP reference · powered by LLaMA 3.3 70B")

    m1, m2, m3 = st.columns([5, 5, 2])
    with m1: crop_name = st.text_input("🌾 Crop", placeholder="e.g. Wheat, Cotton, Onion")
    with m2: mandi     = st.text_input("📍 Mandi / Location", placeholder="e.g. Nashik APMC")
    with m3:
        st.markdown("<br>", unsafe_allow_html=True)
        get_fc = st.button("Forecast →", type="primary", use_container_width=True)

    if get_fc:
        if not crop_name or not mandi:
            st.warning("Enter both a crop and a location.")
        else:
            with st.spinner("Generating AI forecast…"):
                data = _post("/market/forecast", {"crop":crop_name,"location":mandi})
            if data:
                trend = data.get("trend","stable")
                cur   = float(data.get("current_price_per_kg",0))
                p7d   = float(data.get("predicted_price_7d",0))
                p30d  = float(data.get("predicted_price_30d",0))

                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Current Price",   f"₹{cur}/kg")
                mc2.metric("7-Day Forecast",  f"₹{p7d}/kg",
                           delta=f"{'+' if p7d>=cur else ''}{round(p7d-cur,2)}")
                mc3.metric("30-Day Forecast", f"₹{p30d}/kg",
                           delta=f"{'+' if p30d>=cur else ''}{round(p30d-cur,2)}")

                _sec("Price Trend ₹/kg")
                chart_df = pd.DataFrame(
                    {"₹/kg":[cur,p7d,p30d]},
                    index=["Today","+7 Days","+30 Days"]
                )
                st.line_chart(chart_df, use_container_width=True, height=210)

                ti = TREND_ICON.get(trend,"➡️")
                bw = data.get("best_sell_window","")
                st.info(f"{ti} **Trend:** {trend.capitalize()} &nbsp;·&nbsp; 🗓️ **Best window:** {bw}")

                if data.get("price_factors"):
                    with st.expander("📖 AI Price Reasoning"):
                        st.markdown(data["price_factors"])

# ─────────────────────────────────────────
# TAB 5 — SCHEMES
# ─────────────────────────────────────────
SCHEME_DIRECTORY = [
    # ── Income & Direct Benefit ──────────────────────────────────────────────
    {"cat":"Income & Direct Benefit",
     "name":"PM-KISAN",       "full_name":"Pradhan Mantri Kisan Samman Nidhi",                    "url":"https://pmkisan.gov.in"},
    {"cat":"Income & Direct Benefit",
     "name":"PMKMY",          "full_name":"Pradhan Mantri Kisan Maandhan Yojana (Pension)",        "url":"https://maandhan.in/pmkmy"},
    {"cat":"Income & Direct Benefit",
     "name":"PMJDY",          "full_name":"Pradhan Mantri Jan Dhan Yojana",                        "url":"https://pmjdy.gov.in"},

    # ── Crop Insurance ───────────────────────────────────────────────────────
    {"cat":"Crop Insurance",
     "name":"PMFBY",          "full_name":"Pradhan Mantri Fasal Bima Yojana",                      "url":"https://pmfby.gov.in"},
    {"cat":"Crop Insurance",
     "name":"RWBCIS",         "full_name":"Restructured Weather Based Crop Insurance Scheme",      "url":"https://pmfby.gov.in"},

    # ── Credit & Finance ─────────────────────────────────────────────────────
    {"cat":"Credit & Finance",
     "name":"KCC",            "full_name":"Kisan Credit Card",                                     "url":"https://www.nabard.org/content1.aspx?id=572"},
    {"cat":"Credit & Finance",
     "name":"AIF",            "full_name":"Agriculture Infrastructure Fund",                       "url":"https://agriinfra.dac.gov.in"},
    {"cat":"Credit & Finance",
     "name":"NABARD RIDF",    "full_name":"Rural Infrastructure Development Fund",                 "url":"https://www.nabard.org"},

    # ── Irrigation & Water ───────────────────────────────────────────────────
    {"cat":"Irrigation & Water",
     "name":"PMKSY",          "full_name":"Pradhan Mantri Krishi Sinchayee Yojana",                "url":"https://pmksy.gov.in"},
    {"cat":"Irrigation & Water",
     "name":"PMKSY-PDMC",     "full_name":"Per Drop More Crop (Micro Irrigation)",                 "url":"https://pmksy.gov.in/microIrrigation"},
    {"cat":"Irrigation & Water",
     "name":"PMKSY-HKKP",     "full_name":"Har Khet Ko Pani",                                      "url":"https://pmksy.gov.in/hkkp"},
    {"cat":"Irrigation & Water",
     "name":"PMKSY-WDC",      "full_name":"Watershed Development Component",                       "url":"https://dolr.gov.in"},

    # ── Soil & Organic Farming ───────────────────────────────────────────────
    {"cat":"Soil & Organic Farming",
     "name":"SHC",            "full_name":"Soil Health Card Scheme",                               "url":"https://soilhealth.dac.gov.in"},
    {"cat":"Soil & Organic Farming",
     "name":"PKVY",           "full_name":"Paramparagat Krishi Vikas Yojana",                      "url":"https://pgsindia-ncof.gov.in/pkvy/index.aspx"},
    {"cat":"Soil & Organic Farming",
     "name":"NMSA",           "full_name":"National Mission for Sustainable Agriculture",           "url":"https://nmsa.dac.gov.in"},
    {"cat":"Soil & Organic Farming",
     "name":"BSF",            "full_name":"Bhartiya Prakritik Krishi Paddhati (Natural Farming)",  "url":"https://pgsindia-ncof.gov.in"},

    # ── Mechanization & Technology ───────────────────────────────────────────
    {"cat":"Mechanization & Technology",
     "name":"SMAM",           "full_name":"Sub-Mission on Agricultural Mechanization",             "url":"https://agrimachinery.nic.in"},
    {"cat":"Mechanization & Technology",
     "name":"ATMA",           "full_name":"Agricultural Technology Management Agency",             "url":"https://atma-india.net"},
    {"cat":"Mechanization & Technology",
     "name":"NMAET",          "full_name":"National Mission on Agricultural Extension & Technology","url":"https://agricoop.nic.in"},
    {"cat":"Mechanization & Technology",
     "name":"Digital Agri",   "full_name":"Digital Agriculture Mission",                           "url":"https://agricoop.gov.in/en/digitalagriculture"},

    # ── Horticulture ─────────────────────────────────────────────────────────
    {"cat":"Horticulture",
     "name":"MIDH",           "full_name":"Mission for Integrated Development of Horticulture",    "url":"https://midh.gov.in"},
    {"cat":"Horticulture",
     "name":"NHM",            "full_name":"National Horticulture Mission",                         "url":"https://nhm.nic.in"},
    {"cat":"Horticulture",
     "name":"HMNEH",          "full_name":"Horticulture Mission for North East & Himalayan States", "url":"https://nhm.nic.in"},

    # ── Food Security & Crops ────────────────────────────────────────────────
    {"cat":"Food Security & Crops",
     "name":"NFSM",           "full_name":"National Food Security Mission",                        "url":"https://nfsm.gov.in"},
    {"cat":"Food Security & Crops",
     "name":"NMOOP",          "full_name":"National Mission on Oilseeds and Oil Palm",             "url":"https://nmoop.gov.in"},
    {"cat":"Food Security & Crops",
     "name":"ISOPOM",         "full_name":"Integrated Scheme on Oilseeds, Pulses, Oil Palm & Maize","url":"https://agricoop.nic.in"},
    {"cat":"Food Security & Crops",
     "name":"NMoOP",          "full_name":"National Mission on Edible Oils – Oil Palm (NMEO-OP)",  "url":"https://nmeo-op.gov.in"},

    # ── Market & Infrastructure ──────────────────────────────────────────────
    {"cat":"Market & Infrastructure",
     "name":"eNAM",           "full_name":"National Agriculture Market",                           "url":"https://enam.gov.in"},
    {"cat":"Market & Infrastructure",
     "name":"RKVY",           "full_name":"Rashtriya Krishi Vikas Yojana",                         "url":"https://rkvy.nic.in"},
    {"cat":"Market & Infrastructure",
     "name":"SAMPADA",        "full_name":"PM Scheme for Agro-Marine Processing & Development",    "url":"https://mofpi.gov.in/pmksy"},
    {"cat":"Market & Infrastructure",
     "name":"PLI – Food",     "full_name":"Production Linked Incentive Scheme for Food Processing","url":"https://mofpi.gov.in/pli"},
    {"cat":"Market & Infrastructure",
     "name":"GrAM",           "full_name":"Gramin Agricultural Markets (GrAMs)",                   "url":"https://agricoop.nic.in"},

    # ── Fisheries & Animal Husbandry ─────────────────────────────────────────
    {"cat":"Fisheries & Animal Husbandry",
     "name":"PMMSY",          "full_name":"Pradhan Mantri Matsya Sampada Yojana",                  "url":"https://pmmsy.dof.gov.in"},
    {"cat":"Fisheries & Animal Husbandry",
     "name":"AHIDF",          "full_name":"Animal Husbandry Infrastructure Development Fund",      "url":"https://ahidf.udyamimitra.in"},
    {"cat":"Fisheries & Animal Husbandry",
     "name":"NPDD",           "full_name":"National Programme for Dairy Development",              "url":"https://dahd.nic.in"},
    {"cat":"Fisheries & Animal Husbandry",
     "name":"RKVY-REAH",      "full_name":"RKVY – Remunerative Approaches for Agriculture & Allied Sectors","url":"https://rkvy.nic.in"},

    # ── Rural & Allied ───────────────────────────────────────────────────────
    {"cat":"Rural & Allied",
     "name":"MGNREGS",        "full_name":"Mahatma Gandhi National Rural Employment Guarantee Scheme","url":"https://nrega.nic.in"},
    {"cat":"Rural & Allied",
     "name":"PMGSY",          "full_name":"Pradhan Mantri Gram Sadak Yojana",                      "url":"https://pmgsy.nic.in"},
    {"cat":"Rural & Allied",
     "name":"DAY-NRLM",       "full_name":"Deendayal Antyodaya Yojana – National Rural Livelihoods Mission","url":"https://aajeevika.gov.in"},
    {"cat":"Rural & Allied",
     "name":"PMAY-G",         "full_name":"Pradhan Mantri Awaas Yojana – Gramin",                  "url":"https://pmayg.nic.in"},
]

with tab5:
    st.subheader("Government Scheme Finder")
    st.caption("Central & state schemes — PM-KISAN · PMFBY · KCC · Soil Health Card and more")

    finder_tab, list_tab = st.tabs(["🔎 Find Schemes", "📋 Scheme List"])

    with list_tab:
        _sec("All Government Schemes")
        st.caption("Quick reference — scheme names and official websites")
        # group by category
        from itertools import groupby
        sorted_schemes = sorted(SCHEME_DIRECTORY, key=lambda x: x["cat"])
        for cat_name, group in groupby(sorted_schemes, key=lambda x: x["cat"]):
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:0.82rem;font-weight:700;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin:18px 0 8px">{cat_name}</div>', unsafe_allow_html=True)
            for s in group:
                st.markdown(
                    f'<div class="sc-card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;padding:12px 18px">'
                    f'<div>'
                    f'<div class="sc-name" style="margin-bottom:2px;font-size:0.95rem">📋 {s["name"]}</div>'
                    f'<div style="font-size:0.82rem;color:#86efac88">{s["full_name"]}</div>'
                    f'</div>'
                    f'<a href="{s["url"]}" target="_blank" style="'
                    f'background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);'
                    f'border-radius:999px;color:#4ade80;font-size:0.78rem;font-weight:600;'
                    f'padding:5px 14px;text-decoration:none;white-space:nowrap">'
                    f'🌐 Visit</a>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    with finder_tab:
        query = st.text_input("🔍 What are you looking for?",
            placeholder="e.g. crop insurance, drip irrigation subsidy, organic farming")

        s1, s2, s3 = st.columns(3)
        with s1: state  = st.text_input("🗺️ State",  placeholder="e.g. Maharashtra")
        with s2: s_crop = st.text_input("🌾 Crop",   placeholder="e.g. Cotton")
        with s3: cat    = st.selectbox("👨‍🌾 Farmer Category", ["small","marginal","large"])

        if st.button("🔎 Find Schemes", type="primary", use_container_width=True):
            if not query:
                st.warning("Enter what you are looking for.")
            else:
                with st.spinner("Searching database…"):
                    data = _post("/schemes/search", {
                        "query":query,"state":state or None,
                        "crop":s_crop or None,"farmer_category":cat,
                    })
                if data:
                    if data.get("summary"):
                        st.info(data["summary"])

                    schemes = data.get("schemes",[])
                    if not schemes:
                        st.info("No matching schemes found — try broader keywords.")

                    _sec(f"Schemes Found · {len(schemes)} results")
                    for s in schemes:
                        badges = ""
                        if s.get("ministry"):
                            badges += f'<span class="sc-badge">🏛️ {s["ministry"]}</span>'
                        badges += f'<span class="sc-badge">👨‍🌾 {cat}</span>'
                        if s_crop:
                            badges += f'<span class="sc-badge">🌾 {s_crop}</span>'
                        st.markdown(
                            f'<div class="sc-card">'
                            f'<div class="sc-name">📋 {s["name"]} — {s.get("full_name","")}</div>'
                            f'<div style="margin:6px 0 10px">{badges}</div>'
                            f'<div style="font-size:0.9rem;color:#c4e8d1"><b style="color:#86efac">Benefit:</b> {s.get("benefit","")}</div>'
                            f'<div style="font-size:0.86rem;color:#86efac88;margin-top:6px">'
                            f'<b style="color:#86efac55">How to Apply:</b> {s.get("how_to_apply","")}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

# ─────────────────────────────────────────
# TAB 6 — WEATHER
# ─────────────────────────────────────────
with tab6:
    st.subheader("Detailed Weather Report")
    w    = st.session_state.weather_data
    w_er = st.session_state.weather_error

    if w_er and not w:
        st.error(f"Weather unavailable: {w_er}")
        st.info("Update the city in the location box at the top.")
    elif not w:
        st.info("Enter a city in the location box at the top of the page.")
    else:
        for alert in w.get("alerts",[]):
            st.warning(alert)

        _sec("Current Conditions")
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("🌡️ Temp",    f"{w['temp']}°C",             f"Feels {w.get('feels_like',w['temp'])}°C")
        c2.metric("💧 Humidity",f"{w['humidity']}%")
        c3.metric("💨 Wind",    f"{w['wind']} km/h")
        c4.metric("☀️ UV Index",str(w.get("uv_index","—")))
        c5.metric("🌧️ Rain",    f"{w.get('rain_now',0)} mm")
        c6.metric("🔵 Pressure",f"{w.get('pressure','—')} hPa")

        _sec("10-Day Forecast")
        for day in w["forecast"]:
            rp  = day.get("rain_prob",0)
            uv  = day.get("uv",0)
            rc  = "#ef4444" if rp>=70 else "#f97316" if rp>=40 else "#22c55e"
            uvc = "#ef4444" if uv>=9  else "#f97316" if uv>=6  else "#22c55e"
            st.markdown(
                f'<div class="fx-row">'
                f'<div style="min-width:80px;font-weight:600;font-family:DM Sans,sans-serif;color:#ecfdf5">{day["day"]}'
                f'<span style="color:#4ade8033;font-size:11px;margin-left:4px">{day.get("date","")}</span></div>'
                f'<div style="font-size:22px">{day["icon"]}</div>'
                f'<div style="min-width:110px;font-size:13px;color:#86efac">{day.get("desc","")}</div>'
                f'<div style="min-width:80px;font-size:13px;color:#ecfdf5">Max <b>{day["max"]}°C</b> / {day["min"]}°C</div>'
                f'<div style="min-width:100px;font-size:13px;color:#c4e8d1">🌧️ {day.get("rain_mm",0)} mm '
                f'<b style="color:{rc}">{rp}%</b></div>'
                f'<div style="min-width:80px;font-size:13px;color:#86efac88">💨 {day.get("wind_max","—")} km/h</div>'
                f'<div style="min-width:60px;font-size:13px">UV <b style="color:{uvc}">{uv}</b></div>'
                f'<div style="font-size:12px">'
                f'<span style="color:#fbbf24;font-weight:600">🌅 {day.get("sunrise","")}</span>'
                f'<span style="color:#c084fc;font-weight:600;margin-left:10px">🌇 {day.get("sunset","")}</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        _sec("Rain Probability · 10 Days")
        rain_df = pd.DataFrame(
            {"Rain %":[d.get("rain_prob",0) for d in w["forecast"]]},
            index=[d["day"] for d in w["forecast"]],
        )
        st.bar_chart(rain_df, use_container_width=True, height=150)

        _sec("AI Farming Advisory")
        if st.button("Generate Advisory →", type="primary"):
            fs = ", ".join([
                f"{d['day']}: {d.get('desc','')} {d['max']}°/{d['min']}° rain {d.get('rain_prob',0)}%"
                for d in w["forecast"][:5]
            ])
            prompt = (
                f"Location: {w['location']}. Current: {w['temp']}°C, {w['description']}, "
                f"humidity {w['humidity']}%, wind {w['wind']} km/h. "
                f"5-day: {fs}. Give practical farming advisory in 5-6 bullet points: "
                f"best days for sowing/spraying/harvesting, risks, crop protection tips."
            )
            with st.spinner("Generating…"):
                try:
                    rsp = requests.post(f"{API}/chat", json={"message":prompt}, timeout=120)
                    if rsp.status_code == 200:
                        st.markdown(rsp.json().get("reply",""))
                        _audit(datetime.now().strftime("%H:%M:%S"),
                               "/chat [wx-advisory]", {"location":w["location"]}, response=rsp.json())
                    else:
                        st.error("Could not generate advisory.")
                except Exception as exc:
                    st.error(str(exc))

# ─────────────────────────────────────────
# TAB 7 — AUDIT LOG
# ─────────────────────────────────────────
with tab7:
    st.subheader("Agent Decision Audit Log")
    st.caption("Every API call, guardrail trigger, and offline fallback — logged for full auditability")

    audit = st.session_state.audit_log

    if not audit:
        st.info("No entries yet — use the other tabs to generate audit entries.")
    else:
        total_n = len(audit)
        blk_n   = sum(1 for e in audit if e.get("blocked"))
        off_n   = sum(1 for e in audit if e.get("offline"))
        err_n   = sum(1 for e in audit if e["status"]=="ERROR")
        grd_n   = sum(len(e.get("guardrails_triggered",[])) for e in audit)

        # Stats row
        st.markdown(
            f'<div class="stat-row">'
            f'<div class="stat-chip"><div class="v">{total_n}</div><div class="l">Total</div></div>'
            f'<div class="stat-chip"><div class="v" style="color:#22c55e">{total_n-err_n}</div><div class="l">Success</div></div>'
            f'<div class="stat-chip"><div class="v" style="color:#f59e0b">{blk_n}</div><div class="l">Blocked</div></div>'
            f'<div class="stat-chip"><div class="v" style="color:#f59e0b">{off_n}</div><div class="l">Offline</div></div>'
            f'<div class="stat-chip"><div class="v" style="color:#f43f5e">{err_n}</div><div class="l">Errors</div></div>'
            f'<div class="stat-chip"><div class="v" style="color:#f59e0b">{grd_n}</div><div class="l">Guardrails</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        fc1, fc2, fc3 = st.columns([3,1,1])
        with fc1:
            filter_ep = st.multiselect("Filter by endpoint",
                options=sorted({e["endpoint"] for e in audit}), default=[], placeholder="All endpoints")
        with fc2: show_ok  = st.checkbox("Show OK",    value=True, key="ao")
        with fc3: show_err = st.checkbox("Show Errors",value=True, key="ae2")
        st.markdown("""
        <style>
        div[data-testid="stCheckbox"]:has(input[aria-label="Show OK"]) label p,
        div[data-testid="stCheckbox"]:has(input#ao) label p,
        [data-testid="stCheckbox"] label:has(+ div input[value="ao"]) p {
          color: #4ade80 !important; font-weight: 700 !important;
        }
        div[data-testid="stCheckbox"]:has(input[aria-label="Show Errors"]) label p,
        div[data-testid="stCheckbox"]:has(input#ae2) label p {
          color: #f87171 !important; font-weight: 700 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        filtered = [
            e for e in reversed(audit)
            if (not filter_ep or e["endpoint"] in filter_ep)
            and ((show_ok and e["status"]=="OK") or (show_err and e["status"]=="ERROR"))
        ]

        _sec(f"{len(filtered)} Entries · Most Recent First")

        for e in filtered:
            ok     = e["status"] == "OK"
            guards = e.get("guardrails_triggered",[])
            g_html = "".join(f'<span class="ae-guard">🛡️ {g}</span>' for g in guards)
            inp    = json.dumps(e["input"], ensure_ascii=False)
            if len(inp) > 160: inp = inp[:160] + "…"
            err_h  = f'<div class="ae-err-msg">Error: {e["error"]}</div>' if e.get("error") else ""
            pill   = f'<span class="pill-ok">OK</span>' if ok else f'<span class="pill-err">ERROR</span>'

            st.markdown(
                f'<div class="ae {"ae-ok" if ok else "ae-err"}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span class="ae-ep">{e["endpoint"]}</span>'
                f'<span style="display:flex;gap:8px;align-items:center">{pill}'
                f'<span class="ae-ts">{e["time"]}</span></span>'
                f'</div>'
                f'<div class="ae-inp">{inp}</div>'
                f'{"<div style=margin-top:6px>" + g_html + "</div>" if g_html else ""}'
                f'{err_h}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        audit_json = json.dumps(audit, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇️ Export Audit Log (.json)",
            data=audit_json,
            file_name=f"agrigenaai_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:24px 0 8px;border-top:1px solid rgba(34,197,94,0.1);margin-top:20px">
  <span style="font-family:Syne,sans-serif;font-size:1.1rem;color:#4ade80cc;letter-spacing:0.08em;font-weight:600">
    AGRIGENAAI
  </span>
</div>
""", unsafe_allow_html=True)
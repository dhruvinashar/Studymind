import streamlit as st

st.set_page_config(
    page_title="StudyMind CFA",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Libre Baskerville', Georgia, serif !important;
    background-color: #060810 !important;
    color: #ddd8c4 !important;
}
.stApp { background-color: #060810; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0c1a !important;
    border-right: 1px solid #12152a !important;
}
[data-testid="stSidebar"] * { color: #8a8aaa !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f0ead8 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #e8c96a) !important;
    color: #08090f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: .04em !important;
    padding: 8px 20px !important;
    transition: all .2s !important;
}
.stButton > button:hover { box-shadow: 0 6px 24px rgba(201,168,76,.35) !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #0c0f1e !important;
    border: 1px solid #1a1d2e !important;
    color: #ddd8c4 !important;
    border-radius: 6px !important;
    font-family: 'Libre Baskerville', serif !important;
}
.stTextArea > div > div > textarea { line-height: 1.75 !important; }

/* Cards via containers */
[data-testid="stExpander"] {
    background: #0c0f1e !important;
    border: 1px solid #1a1d2e !important;
    border-radius: 10px !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: #0c0f1e;
    border: 1px solid #1a1d2e;
    border-radius: 10px;
    padding: 16px;
}
[data-testid="stMetricValue"] { color: #c9a84c !important; font-family: 'IBM Plex Mono', monospace !important; }
[data-testid="stMetricLabel"] { color: #555878 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; }

/* Divider */
hr { border-color: #12152a !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #080a12 !important;
    border: 1px solid #12152a !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4a4d68 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c9a84c, #e8c96a) !important;
    color: #08090f !important;
    font-weight: 500 !important;
}

/* Success / Info / Warning */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 8px !important;
}

/* Code blocks for formulas */
code {
    background: #080a12 !important;
    color: #e8deb8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #060810; }
::-webkit-scrollbar-thumb { background: #1e2235; border-radius: 2px; }

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding: 20px 0 28px;'>
  <div style='width:52px;height:52px;border-radius:12px;background:linear-gradient(135deg,#c9a84c,#e8c96a);display:inline-flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:10px;'>📚</div>
  <div style='font-size:20px;font-weight:700;color:#f0ead8;letter-spacing:-.02em;'>StudyMind</div>
  <div style='font-size:10px;color:#c9a84c;font-family:"IBM Plex Mono",monospace;letter-spacing:.1em;margin-top:2px;'>CFA EDITION</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Navigate")
st.sidebar.page_link("app.py",            label="🏠  Home / Dashboard")
st.sidebar.page_link("pages/1_notes.py",    label="📝  Smart Notes")
st.sidebar.page_link("pages/2_quiz.py",     label="🧠  Practice Quiz")
st.sidebar.page_link("pages/3_formulas.py", label="∑   Formula Extractor")
st.sidebar.page_link("pages/4_tracker.py",  label="📊  Study Tracker")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")
st.sidebar.page_link("pages/5_settings.py", label="🔑  API Key & Settings")

# ── Home Dashboard ────────────────────────────────────────────────────────────
from db import init_db, get_stats
init_db()

st.markdown("""
<h1 style='font-size:36px;font-weight:700;color:#f0ead8;letter-spacing:-.03em;margin-bottom:4px;'>
  Welcome to StudyMind <span style='color:#c9a84c;font-style:italic;'>CFA</span>
</h1>
<p style='font-family:"IBM Plex Mono",monospace;font-size:12px;color:#353850;margin-bottom:32px;'>
  Your AI-powered study companion for CFA Level I · II · III & Commerce
</p>
""", unsafe_allow_html=True)

stats = get_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("📓 Total Notes",     stats["notes"])
col2.metric("📝 Quizzes Taken",   stats["quizzes"])
col3.metric("⭐ Avg Quiz Score",  f"{stats['avg_score']}%")
col4.metric("🔥 Study Streak",    f"{stats['streak']}d")

st.markdown("---")

st.markdown("""
<h3 style='color:#f0ead8;margin-bottom:16px;'>What would you like to do?</h3>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div style='background:#0c0f1e;border:1px solid #1a1d2e;border-radius:10px;padding:20px;text-align:center;'>
      <div style='font-size:32px;margin-bottom:10px;'>📝</div>
      <div style='font-size:15px;font-weight:700;color:#f0ead8;margin-bottom:6px;'>Smart Notes</div>
      <div style='font-size:12px;color:#444660;'>Paste raw notes → AI generates exam-ready summaries with key formulas & traps</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style='background:#0c0f1e;border:1px solid #1a1d2e;border-radius:10px;padding:20px;text-align:center;'>
      <div style='font-size:32px;margin-bottom:10px;'>🧠</div>
      <div style='font-size:15px;font-weight:700;color:#f0ead8;margin-bottom:6px;'>Practice Quiz</div>
      <div style='font-size:12px;color:#444660;'>CFA-style MCQs with vignettes, explanations, and score tracking</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style='background:#0c0f1e;border:1px solid #1a1d2e;border-radius:10px;padding:20px;text-align:center;'>
      <div style='font-size:32px;margin-bottom:10px;'>∑</div>
      <div style='font-size:15px;font-weight:700;color:#f0ead8;margin-bottom:6px;'>Formula Extractor</div>
      <div style='font-size:12px;color:#444660;'>Auto-extract all CFA formulas & ratios from your notes into a cheat sheet</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div style='background:#0c0f1e;border:1px solid #1a1d2e;border-radius:10px;padding:20px;text-align:center;'>
      <div style='font-size:32px;margin-bottom:10px;'>📊</div>
      <div style='font-size:15px;font-weight:700;color:#f0ead8;margin-bottom:6px;'>Study Tracker</div>
      <div style='font-size:12px;color:#444660;'>Daily progress, streak tracking, and quiz performance history</div>
    </div>""", unsafe_allow_html=True)

if stats["notes"] == 0:
    st.info("👋 Get started by adding your first note! Go to **Smart Notes** in the sidebar.")

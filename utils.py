import os
import json
import streamlit as st
import anthropic

CFA_TOPICS = {
    "Level I": [
        "Ethical & Professional Standards", "Quantitative Methods", "Economics",
        "Financial Statement Analysis", "Corporate Issuers", "Equity Investments",
        "Fixed Income", "Derivatives", "Alternative Investments", "Portfolio Management",
    ],
    "Level II": [
        "Ethical & Professional Standards", "Quantitative Methods", "Economics",
        "Financial Statement Analysis", "Corporate Issuers", "Equity Valuation",
        "Fixed Income", "Derivatives", "Alternative Investments", "Portfolio Management",
    ],
    "Level III": [
        "Ethical & Professional Standards", "Behavioral Finance",
        "Capital Market Expectations", "Asset Allocation",
        "Derivatives & Currency Management", "Fixed Income", "Equity",
        "Alternative Investments", "Portfolio Construction", "Monitoring & Rebalancing",
    ],
    "Commerce / Accounts": [
        "Financial Accounting", "Management Accounting", "Cost Accounting",
        "Auditing", "Taxation", "Corporate Finance", "Financial Reporting",
        "Business Law", "Economics", "Statistics",
    ],
}


def get_client():
    """Return Anthropic client using key from settings or env."""
    api_key = st.session_state.get("api_key") or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("⚠️ No API key found. Go to **Settings** (sidebar) and enter your Anthropic API key.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def call_claude(system: str, user: str, max_tokens: int = 1400) -> str:
    client = get_client()
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


def level_color(level: str) -> str:
    return {
        "Level I":            "#5cb6ff",
        "Level II":           "#c9a84c",
        "Level III":          "#9370db",
        "Commerce / Accounts":"#4ecd96",
    }.get(level, "#8a8aaa")


def level_badge(level: str) -> str:
    color = level_color(level)
    return (
        f"<span style='display:inline-block;padding:2px 10px;border-radius:20px;"
        f"font-family:\"IBM Plex Mono\",monospace;font-size:10px;letter-spacing:.05em;"
        f"background:rgba(0,0,0,.3);color:{color};"
        f"border:1px solid {color}44;'>{level}</span>"
    )


def page_header(title: str, sub: str):
    st.markdown(f"""
    <h1 style='font-size:30px;font-weight:700;color:#f0ead8;letter-spacing:-.03em;margin-bottom:4px;'>{title}</h1>
    <p style='font-family:"IBM Plex Mono",monospace;font-size:11px;color:#353850;margin-bottom:28px;'>{sub}</p>
    """, unsafe_allow_html=True)


def sidebar_nav():
    st.sidebar.markdown("""
    <div style='text-align:center; padding: 20px 0 28px;'>
      <div style='width:52px;height:52px;border-radius:12px;background:linear-gradient(135deg,#c9a84c,#e8c96a);
           display:inline-flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:10px;'>📚</div>
      <div style='font-size:20px;font-weight:700;color:#f0ead8;letter-spacing:-.02em;'>StudyMind</div>
      <div style='font-size:10px;color:#c9a84c;font-family:"IBM Plex Mono",monospace;letter-spacing:.1em;margin-top:2px;'>CFA EDITION</div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 Navigate")
    st.sidebar.page_link("app.py",              label="🏠  Home / Dashboard")
    st.sidebar.page_link("pages/1_notes.py",    label="📝  Smart Notes")
    st.sidebar.page_link("pages/2_quiz.py",     label="🧠  Practice Quiz")
    st.sidebar.page_link("pages/3_formulas.py", label="∑   Formula Extractor")
    st.sidebar.page_link("pages/4_tracker.py",  label="📊  Study Tracker")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")
    st.sidebar.page_link("pages/5_settings.py", label="🔑  API Key & Settings")

# 📚 StudyMind CFA — AI Study Companion

A Streamlit-based AI study tool built for **CFA Level I / II / III** and **Commerce / Accounts** students.

## Features

| Feature | Description |
|---|---|
| 📝 Smart Notes | Paste raw notes → AI generates exam-ready summaries with Core Concepts, Formulas, Exam Traps & Quick Revision |
| 🧠 Practice Quiz | CFA-style MCQs (3–10 questions) with vignettes, explanations, score tracking & retake history |
| ∑ Formula Extractor | Auto-extracts all formulas, ratios & equations from your notes, grouped by category |
| 📊 Study Tracker | Daily progress, 14-day activity chart, streak counter, quiz performance history |

## Setup

### 1. Install dependencies
```bash
pip install streamlit anthropic plotly
```

### 2. Get your Anthropic API key
- Go to [console.anthropic.com](https://console.anthropic.com)
- Create an API key (starts with `sk-ant-`)

### 3. Set your API key
```bash
# Option A: environment variable
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Option B: create .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

### 4. Run
```bash
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select your repo, set `app.py` as the entry point
4. Under **Advanced → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Deploy! ✅

## Project Structure

```
studymind/
├── app.py                  ← Home dashboard (entry point)
├── db.py                   ← SQLite database layer
├── utils.py                ← AI helpers, CFA taxonomy, shared UI
├── requirements.txt
├── studymind.db            ← Auto-created on first run
├── .streamlit/
│   └── config.toml         ← Dark theme config
└── pages/
    ├── 1_notes.py          ← Smart Notes
    ├── 2_quiz.py           ← Practice Quiz
    ├── 3_formulas.py       ← Formula Extractor
    ├── 4_tracker.py        ← Study Tracker
    └── 5_settings.py       ← API Key & Settings
```

## CFA Topics Covered

- **Level I**: Ethics, Quant, Economics, FSA, Corporate Issuers, Equity, Fixed Income, Derivatives, Alternatives, Portfolio Mgmt
- **Level II**: Same + Equity Valuation (vignette-style questions)
- **Level III**: Ethics, Behavioral Finance, CME, Asset Allocation, Derivatives, Fixed Income, Equity, Alternatives, Portfolio Construction
- **Commerce**: Financial Accounting, Management Accounting, Cost Accounting, Auditing, Taxation, Corporate Finance, and more

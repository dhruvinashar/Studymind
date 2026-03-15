import sqlite3
import json
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "studymind.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        title     TEXT NOT NULL,
        raw       TEXT NOT NULL,
        summary   TEXT,
        level     TEXT,
        topic     TEXT,
        created   TEXT DEFAULT (date('now'))
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id     INTEGER,
        note_title  TEXT,
        level       TEXT,
        topic       TEXT,
        questions   TEXT NOT NULL,
        last_score  INTEGER DEFAULT NULL,
        total_q     INTEGER,
        created     TEXT DEFAULT (date('now')),
        FOREIGN KEY(note_id) REFERENCES notes(id) ON DELETE SET NULL
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS formula_sheets (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id     INTEGER,
        note_title  TEXT,
        level       TEXT,
        topic       TEXT,
        formulas    TEXT NOT NULL,
        created     TEXT DEFAULT (date('now')),
        FOREIGN KEY(note_id) REFERENCES notes(id) ON DELETE SET NULL
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS tracker (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        day         TEXT NOT NULL,
        notes_added INTEGER DEFAULT 0,
        quizzes_done INTEGER DEFAULT 0,
        correct     INTEGER DEFAULT 0,
        total_q     INTEGER DEFAULT 0,
        UNIQUE(day)
    )""")

    conn.commit()
    conn.close()


# ── Notes ─────────────────────────────────────────────────────────────────────
def add_note(title, raw, summary, level, topic):
    conn = get_conn()
    conn.execute(
        "INSERT INTO notes (title, raw, summary, level, topic) VALUES (?,?,?,?,?)",
        (title, raw, summary, level, topic)
    )
    conn.commit()
    conn.close()
    bump_tracker("notes_added", 1)


def get_notes():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_note(note_id):
    conn = get_conn()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()


# ── Quizzes ───────────────────────────────────────────────────────────────────
def add_quiz(note_id, note_title, level, topic, questions):
    conn = get_conn()
    conn.execute(
        "INSERT INTO quizzes (note_id, note_title, level, topic, questions, total_q) VALUES (?,?,?,?,?,?)",
        (note_id, note_title, level, topic, json.dumps(questions), len(questions))
    )
    conn.commit()
    conn.close()


def get_quizzes():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM quizzes ORDER BY id DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["questions"] = json.loads(d["questions"])
        result.append(d)
    return result


def update_quiz_score(quiz_id, score):
    conn = get_conn()
    conn.execute("UPDATE quizzes SET last_score=? WHERE id=?", (score, quiz_id))
    conn.commit()
    conn.close()
    bump_tracker("quizzes_done", 1)
    bump_tracker("correct", score)


def delete_quiz(quiz_id):
    conn = get_conn()
    conn.execute("DELETE FROM quizzes WHERE id=?", (quiz_id,))
    conn.commit()
    conn.close()


# ── Formula Sheets ─────────────────────────────────────────────────────────────
def save_formula_sheet(note_id, note_title, level, topic, formulas):
    conn = get_conn()
    conn.execute("DELETE FROM formula_sheets WHERE note_id=?", (note_id,))
    conn.execute(
        "INSERT INTO formula_sheets (note_id, note_title, level, topic, formulas) VALUES (?,?,?,?,?)",
        (note_id, note_title, level, topic, json.dumps(formulas))
    )
    conn.commit()
    conn.close()


def get_formula_sheets():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM formula_sheets ORDER BY id DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["formulas"] = json.loads(d["formulas"])
        result.append(d)
    return result


# ── Tracker ───────────────────────────────────────────────────────────────────
def bump_tracker(col, n=1):
    today = date.today().isoformat()
    conn = get_conn()
    conn.execute(
        f"INSERT INTO tracker(day, {col}) VALUES(?,?) "
        f"ON CONFLICT(day) DO UPDATE SET {col}={col}+?",
        (today, n, n)
    )
    conn.commit()
    conn.close()


def get_tracker_days(n=14):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM tracker ORDER BY day DESC LIMIT ?", (n,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_today_stats():
    today = date.today().isoformat()
    conn = get_conn()
    row = conn.execute("SELECT * FROM tracker WHERE day=?", (today,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"notes_added": 0, "quizzes_done": 0, "correct": 0, "total_q": 0}


def get_stats():
    conn = get_conn()
    notes_count  = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    quizzes_done = conn.execute("SELECT COUNT(*) FROM quizzes WHERE last_score IS NOT NULL").fetchone()[0]
    avg_row      = conn.execute(
        "SELECT AVG(CAST(last_score AS FLOAT)/total_q)*100 FROM quizzes WHERE last_score IS NOT NULL AND total_q>0"
    ).fetchone()[0]
    conn.close()

    avg_score = round(avg_row) if avg_row else 0

    # Streak
    streak = 0
    d = date.today()
    conn2 = get_conn()
    for _ in range(365):
        row = conn2.execute(
            "SELECT notes_added+quizzes_done as activity FROM tracker WHERE day=?",
            (d.isoformat(),)
        ).fetchone()
        if row and row["activity"] > 0:
            streak += 1
            d -= timedelta(days=1)
        else:
            break
    conn2.close()

    return {
        "notes": notes_count,
        "quizzes": quizzes_done,
        "avg_score": avg_score,
        "streak": streak,
    }

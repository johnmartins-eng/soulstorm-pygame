import sqlite3
import threading
from datetime import datetime
from typing import List, Tuple

DB_PATH = "data/game.db"


def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


_init_lock = threading.Lock()
_initialized = False


def init_db():
    global _initialized
    with _init_lock:
        if _initialized:
            return
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                ts TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS best_scores (
                user_id INTEGER PRIMARY KEY,
                score INTEGER NOT NULL,
                ts TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        conn.commit()
        conn.close()
        _initialized = True


def get_or_create_user(username: str) -> int:
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row:
        uid = row["id"]
        conn.close()
        return uid
    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid


def add_score(user_id: int, score: int):
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    ts = datetime.utcnow().isoformat()
    # Always record the score in historical table
    cur.execute("INSERT INTO scores (user_id, score, ts) VALUES (?, ?, ?)", (user_id, score, ts))

    # Update best_scores: if no record exists, insert; if exists and new score is greater, update
    cur.execute("SELECT score FROM best_scores WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO best_scores (user_id, score, ts) VALUES (?, ?, ?)", (user_id, score, ts))
    else:
        best = row["score"]
        if score > best:
            cur.execute("UPDATE best_scores SET score = ?, ts = ? WHERE user_id = ?", (score, ts, user_id))

    conn.commit()
    conn.close()


def get_top_scores(limit: int = 10) -> List[Tuple[str, int, str]]:
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    # Use best_scores to show the top record per user
    cur.execute(
        """
        SELECT u.username as username, b.score as score, b.ts as ts
        FROM best_scores b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.score DESC, b.ts ASC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cur.fetchall()
    result = [(r["username"], r["score"], r["ts"]) for r in rows]
    conn.close()
    return result


def get_user_best(user_id: int):
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT score, ts FROM best_scores WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row["score"], row["ts"]
    return None

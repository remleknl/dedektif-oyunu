import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent / "data" / "game.db"
SCHEMA   = Path(__file__).parent / "schema.sql"
SEED     = Path(__file__).parent / "seed.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(seed: bool = False) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        if seed:
            conn.executescript(SEED.read_text(encoding="utf-8"))


# ── Odalar ────────────────────────────────────────────────────────────────────

def get_all_rooms() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM rooms ORDER BY id").fetchall()


def get_room(room_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()


# ── İpuçları ──────────────────────────────────────────────────────────────────

def get_clues_in_room(room_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM clues WHERE room_id = ? ORDER BY id", (room_id,)
        ).fetchall()


def get_clue(clue_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM clues WHERE id = ?", (clue_id,)).fetchone()


# ── Şüpheliler ────────────────────────────────────────────────────────────────

def get_all_suspects() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM suspects ORDER BY id").fetchall()


def get_suspect(suspect_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM suspects WHERE id = ?", (suspect_id,)
        ).fetchone()


# ── İfadeler ──────────────────────────────────────────────────────────────────

def get_initial_statements(suspect_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM statements WHERE suspect_id = ? AND trigger_type = 'initial'",
            (suspect_id,),
        ).fetchall()


def get_triggered_statements(suspect_id: int, clue_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """SELECT * FROM statements
               WHERE suspect_id = ? AND trigger_type = 'after_clue' AND trigger_clue = ?""",
            (suspect_id, clue_id),
        ).fetchall()


def get_confronted_statements(suspect_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM statements WHERE suspect_id = ? AND trigger_type = 'confronted'",
            (suspect_id,),
        ).fetchall()


# ── Çelişkiler ────────────────────────────────────────────────────────────────

def get_contradiction(statement_id: int, clue_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """SELECT * FROM contradictions
               WHERE statement_id = ? AND clue_id = ?""",
            (statement_id, clue_id),
        ).fetchone()


# ── Oyun Oturumu ──────────────────────────────────────────────────────────────

def create_session(player_name: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO game_sessions (player_name) VALUES (?)", (player_name,)
        )
        return cur.lastrowid


def get_session(session_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM game_sessions WHERE id = ?", (session_id,)
        ).fetchone()


def collect_clue(session_id: int, clue_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO session_clues (session_id, clue_id) VALUES (?, ?)",
            (session_id, clue_id),
        )


def get_collected_clue_ids(session_id: int) -> set[int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT clue_id FROM session_clues WHERE session_id = ?", (session_id,)
        ).fetchall()
        return {r["clue_id"] for r in rows}


def record_interrogation(session_id: int, suspect_id: int, statement_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO session_interrogations (session_id, suspect_id, statement_id)
               VALUES (?, ?, ?)""",
            (session_id, suspect_id, statement_id),
        )


def catch_contradiction(session_id: int, contradiction_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO session_contradictions (session_id, contradiction_id) VALUES (?, ?)",
            (session_id, contradiction_id),
        )


def get_caught_contradiction_ids(session_id: int) -> set[int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT contradiction_id FROM session_contradictions WHERE session_id = ?",
            (session_id,),
        ).fetchall()
        return {r["contradiction_id"] for r in rows}


def accuse(session_id: int, suspect_id: int) -> bool:
    suspect = get_suspect(suspect_id)
    won = bool(suspect and suspect["is_killer"])
    status = "won" if won else "lost"
    with get_connection() as conn:
        conn.execute(
            """UPDATE game_sessions
               SET status = ?, accusation_suspect_id = ?, completed_at = datetime('now')
               WHERE id = ?""",
            (status, suspect_id, session_id),
        )
    return won

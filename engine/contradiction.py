import sqlite3
from typing import Optional
from db import db


def confront(session_id: int, statement_id: int, clue_id: int) -> Optional[dict]:
    """
    Oyuncu bir ifadeyi topladığı bir ipucuyla yüzleştirdiğinde çağrılır.
    Çelişki varsa kayıt eder ve şu sözlüğü döner:
        {"contradiction_id": int, "explanation": str}
    Çelişki yoksa None döner.
    """
    contradiction = db.get_contradiction(statement_id, clue_id)
    if contradiction is None:
        return None

    db.catch_contradiction(session_id, contradiction["id"])
    return {
        "contradiction_id": contradiction["id"],
        "explanation": contradiction["explanation"],
    }


def get_caught_contradictions(session_id: int) -> list[sqlite3.Row]:
    """Oturumda yakalanmış tüm çelişkileri döner."""
    caught_ids = db.get_caught_contradiction_ids(session_id)
    with db.get_connection() as conn:
        return [
            conn.execute(
                """SELECT c.*, s.content AS statement_content, cl.name AS clue_name
                   FROM contradictions c
                   JOIN statements s  ON s.id  = c.statement_id
                   JOIN clues     cl ON cl.id = c.clue_id
                   WHERE c.id = ?""",
                (cid,),
            ).fetchone()
            for cid in sorted(caught_ids)
        ]

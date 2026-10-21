import sqlite3
from db import db


def confront(session_id: int, statement_id: int, clue_id: int) -> dict | None:
    """
    Oyuncu bir ifadeyi topladığı bir ipucuyla yüzleştirdiğinde çağrılır.
    Çelişki varsa kayıt eder ve şu sözlüğü döner:
        {"contradiction_id": int, "explanation": str}
    Çelişki yoksa None döner.
    """
    raise NotImplementedError


def get_caught_contradictions(session_id: int) -> list[sqlite3.Row]:
    """Oturumda yakalanmış tüm çelişkileri döner."""
    raise NotImplementedError

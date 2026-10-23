import sqlite3
from db import db


def start_game(player_name: str) -> int:
    """Yeni oyun oturumu başlatır, session_id döner."""
    return db.create_session(player_name)


def get_state(session_id: int) -> dict:
    """
    Mevcut oyun durumunu döner:
    {
        "session": sqlite3.Row,
        "collected_clue_ids": set[int],
        "caught_contradiction_ids": set[int],
    }
    """
    return {
        "session": db.get_session(session_id),
        "collected_clue_ids": db.get_collected_clue_ids(session_id),
        "caught_contradiction_ids": db.get_caught_contradiction_ids(session_id),
    }


def finish_game(session_id: int, suspect_id: int) -> bool:
    """Şüpheliyi suçlar; kazandıysa True döner."""
    return db.accuse(session_id, suspect_id)

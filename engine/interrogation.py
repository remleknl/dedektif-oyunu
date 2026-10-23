import sqlite3
from db import db


def get_suspects() -> list[sqlite3.Row]:
    """Tüm şüphelileri döner."""
    return db.get_all_suspects()


def get_available_statements(session_id: int, suspect_id: int) -> list[sqlite3.Row]:
    """
    Oyuncunun görebileceği ifadeleri döner:
    - trigger_type = 'initial'    → her zaman görünür
    - trigger_type = 'after_clue' → oyuncu o ipucunu topladıysa görünür
    'confronted' ifadeleri bu fonksiyondan dönmez; yalnızca çelişki
    yakalandığında engine/contradiction.py tetikler.
    """
    statements = list(db.get_initial_statements(suspect_id))

    collected_ids = db.get_collected_clue_ids(session_id)
    for clue_id in collected_ids:
        statements.extend(db.get_triggered_statements(suspect_id, clue_id))

    return statements


def interrogate(session_id: int, suspect_id: int, statement_id: int) -> None:
    """Sorgulamayı kaydeder."""
    db.record_interrogation(session_id, suspect_id, statement_id)

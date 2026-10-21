import sqlite3
from db import db


def get_suspects() -> list[sqlite3.Row]:
    """Tüm şüphelileri döner."""
    raise NotImplementedError


def get_available_statements(session_id: int, suspect_id: int) -> list[sqlite3.Row]:
    """
    Oyuncunun görebileceği ifadeleri döner:
    - trigger_type = 'initial'    → her zaman görünür
    - trigger_type = 'after_clue' → oyuncu o ipucunu topladıysa görünür
    'confronted' ifadeleri bu fonksiyondan dönmez; yalnızca çelişki
    yakalandığında engine/contradiction.py tetikler.
    """
    raise NotImplementedError


def interrogate(session_id: int, suspect_id: int, statement_id: int) -> None:
    """Sorgulamayı kaydeder."""
    raise NotImplementedError

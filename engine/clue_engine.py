import sqlite3
from db import db


def get_rooms() -> list[sqlite3.Row]:
    """Tüm odaları döner."""
    raise NotImplementedError


def get_room_clues(session_id: int, room_id: int) -> list[sqlite3.Row]:
    """
    Odadaki ipuçlarını döner.
    Her satıra `collected` (bool) alanı eklenmeli: oyuncunun bu ipucunu
    toplayıp toplamadığını gösterir.
    """
    raise NotImplementedError


def collect_clue(session_id: int, clue_id: int) -> None:
    """İpucunu oturuma ekler."""
    raise NotImplementedError


def get_collected_clues(session_id: int) -> list[sqlite3.Row]:
    """Oyuncunun topladığı tüm ipuçlarını döner."""
    raise NotImplementedError

import sqlite3
from db import db


def get_rooms() -> list[sqlite3.Row]:
    """Tüm odaları döner."""
    return db.get_all_rooms()


def get_room_clues(session_id: int, room_id: int) -> list[dict]:
    """
    Odadaki ipuçlarını döner.
    Her öğeye `collected` (bool) alanı eklenir: oyuncunun bu ipucunu
    toplayıp toplamadığını gösterir.
    """
    clues = db.get_clues_in_room(room_id)
    collected_ids = db.get_collected_clue_ids(session_id)
    return [
        {**dict(clue), "collected": clue["id"] in collected_ids}
        for clue in clues
    ]


def collect_clue(session_id: int, clue_id: int) -> None:
    """İpucunu oturuma ekler."""
    db.collect_clue(session_id, clue_id)


def get_collected_clues(session_id: int) -> list[sqlite3.Row]:
    """Oyuncunun topladığı tüm ipuçlarını döner."""
    collected_ids = db.get_collected_clue_ids(session_id)
    return [db.get_clue(clue_id) for clue_id in sorted(collected_ids)]

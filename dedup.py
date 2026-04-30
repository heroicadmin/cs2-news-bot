import sqlite3
import datetime
from config import DB_PATH, DEDUP_RETENTION_DAYS


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_items ("
        "item_id TEXT PRIMARY KEY,"
        "seen_at TEXT NOT NULL"
        ")"
    )
    conn.commit()
    return conn


def is_seen(item_id: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_items WHERE item_id = ?", (item_id,)
        ).fetchone()
        return row is not None


def mark_seen(item_id: str) -> None:
    now = datetime.datetime.utcnow().isoformat()
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_items (item_id, seen_at) VALUES (?, ?)",
            (item_id, now),
        )
        conn.commit()


def purge_old() -> int:
    cutoff = (
        datetime.datetime.utcnow() - datetime.timedelta(days=DEDUP_RETENTION_DAYS)
    ).isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            "DELETE FROM seen_items WHERE seen_at < ?", (cutoff,)
        )
        conn.commit()
        return cursor.rowcount

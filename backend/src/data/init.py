"""Initialize and manage SQLite database connections with SpatiaLite support."""

import os
import sqlite3
import logging
import ctypes.util
from pathlib import Path
from contextlib import contextmanager
from typing import Generator


logger = logging.getLogger(__name__)


def get_db_path() -> str:
    """Determine the database file path and ensure the directory exists."""
    top_dir = Path(__file__).resolve().parents[2]
    db_dir = top_dir / "db"
    db_dir.mkdir(parents=True, exist_ok=True)
    return os.getenv("CUPIDS_BOW", str(db_dir / "cupids_bow.db"))


def _load_spatialite(conn: sqlite3.Connection) -> None:
    """Attempt to load SpatiaLite extension using cross-platform fallbacks."""
    conn.enable_load_extension(True)
    
    # Common extension names across operating systems
    candidates = [
        "mod_spatialite",
        ctypes.util.find_library("spatialite"),
        "/usr/lib/x86_64-linux-gnu/mod_spatialite.so",
        "/usr/local/lib/mod_spatialite.dylib",  # macOS Homebrew fallback
    ]
    
    for candidate in filter(None, candidates):
        try:
            conn.load_extension(candidate)
            return
        except sqlite3.OperationalError:
            continue
            
    logger.error("Failed to load SpatiaLite extension from all candidate paths.")
    raise RuntimeError("SpatiaLite extension could not be loaded.")


def init_spatialite_once() -> None:
    """
    Initialize SpatiaLite metadata safely and configure DB performance pragmas.
    Call this ONCE at application startup.
    """
    db_path = get_db_path()
    logger.info("Initializing SpatiaLite metadata at %s", db_path)

    with sqlite3.connect(db_path) as conn:
        _load_spatialite(conn)
        
        # Performance Pragmas: WAL mode for concurrency, foreign keys enabled
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        
        cursor = conn.cursor()
        try:
            # InitSpatialMetaData(1) uses transaction safety
            cursor.execute("SELECT InitSpatialMetaData(1);")
        except sqlite3.OperationalError as e:
            if "already exists" in str(e).lower() or "table" in str(e).lower():
                logger.debug("SpatiaLite metadata tables already present.")
            else:
                logger.error("Error initializing SpatiaLite metadata: %s", e)
                raise


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager yielding a thread-safe connection with auto-commit on success.
    """
    conn = sqlite3.connect(get_db_path(), timeout=10.0)
    conn.row_factory = sqlite3.Row
    
    _load_spatialite(conn)
    
    try:
        with conn:  # Enforces automatic COMMIT on success, ROLLBACK on exception
            yield conn
    finally:
        conn.close()
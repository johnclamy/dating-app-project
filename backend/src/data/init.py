"""Initialize and manage SQLite database connections"""

import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator


def get_db_path() -> str:
    """Determine the database file path and ensure the directory exists."""
    # This file is in backend/src/data/
    # parents[2] resolves up to the backend/ directory
    top_dir = Path(__file__).resolve().parents[2]
    db_dir = top_dir / "db"
    db_dir.mkdir(parents=True, exist_ok=True)
    return os.getenv("CUPIDS_BOW", str(db_dir / "cupids_bow.db"))


def init_spatialite_once():
    """
    Initialize SpatiaLite metadata safely.
    Call this exactly ONCE at application startup (e.g., in main.py).
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    
    try:
        conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
    except sqlite3.OperationalError:
        conn.load_extension("mod_spatialite")
    
    cursor = conn.cursor()
    try:
        # Attempt to initialize metadata
        cursor.execute("SELECT InitSpatialMetaData(1);")
        conn.commit()
    except sqlite3.OperationalError as e:
        # Safely ignore the error if the tables already exist
        if "already exists" not in str(e).lower():
            raise
    finally:
        conn.close()


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager to yield a fresh database connection per request.
    This prevents "closed database" errors in async/multi-threaded environments.
    """
    conn = sqlite3.connect(get_db_path())
    conn.enable_load_extension(True)
    
    # Enables dict-like access to columns (e.g., row["id"] instead of row[0])
    conn.row_factory = sqlite3.Row 
    
    try:
        conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
    except sqlite3.OperationalError:
        conn.load_extension("mod_spatialite")
        
    try:
        yield conn
    finally:
        # Always close the connection when the request is done
        conn.close()
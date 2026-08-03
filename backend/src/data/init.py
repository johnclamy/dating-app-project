"""Initialize SQLite database"""

import os
import sqlite3
from pathlib import Path
from sqlite3 import Connection, connect, Cursor


conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False) -> None:
    """Connect to SQLite database file"""
    global conn, curs
    
    if conn:
        if not reset:
            return

        conn.close() # Close the existing connection before resetting
        curs = None
        conn = None

    if not name:
        # Note: parents[0] is 'data', parents[1] is 'src', parents[2] is 'backend'  
        top_dir = Path(__file__).resolve().parents[2]  # This will point to the 'backend' directory
        db_dir = top_dir / "db"

        # Create a directory if it doesn't exist ---
        db_dir.mkdir(parents=True, exist_ok=True)

        db_name = "cupids_bow.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CUPIDS_BOW", db_path)

    # Check path is resolving as expected
    print(f"Connecting to SQLite DB at: {name}")

    # Enable extension loading on the connection
    conn = connect(name, check_same_thread=False)
    conn.enable_load_extension(True)

    # Load the SpatiaLite library
    try:
        conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
        print("SpatiaLite extension loaded via direct path!")
    except sqlite3.OperationalError:
        try:
            conn.load_extension("mod_spatialite")
            print("SpatiaLite extension loaded via system shortcut!")
        except sqlite3.OperationalError as e:
            print(f"Failed to load SpatiaLite extension: {e}")
            conn.close()
            raise    

    # Initialize spatial metadata tables
    curs = conn.cursor()
    # '1' accelerates initialization on modern SpatiaLite (4.3+)
    curs.execute("SELECT InitSpatialMetaData(1);")
    conn.commit()


# Run initialization
get_db()

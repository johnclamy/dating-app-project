import uuid
import sqlite3
from datetime import date, datetime
from typing import List, Optional
from model.location import Location
from model.users import User, Gender, LookingFor
from .init import get_db_connection


def init_db_schema() -> None:
    """Create the users table with SpatiaLite geometry support. Call this once at startup."""
    with get_db_connection() as conn:
        curs = conn.cursor()

        # 1. Create the base table
        curs.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                gender TEXT NOT NULL,
                looking_for TEXT NOT NULL,
                bio TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        # 2. Add SpatiaLite geometry column (this is idempotent/safe to run multiple times)
        try:
            curs.execute("SELECT AddGeometryColumn('users', 'location', 4326, 'POINT', 'XY')")
            conn.commit()
        except Exception:
            pass  # Column likely already exists, which is perfectly fine


def _row_to_user(row: dict) -> User:
    """Helper to safely convert a flat DB row dict into a nested Pydantic User model."""
    return User(
        id=uuid.UUID(row["id"]),
        first_name=row["first_name"],
        last_name=row["last_name"],
        date_of_birth=date.fromisoformat(row["date_of_birth"]),
        email=row["email"],
        gender=Gender(row["gender"]),
        looking_for=LookingFor(row["looking_for"]),

        # Reconstruct the nested Location model from the flattened DB columns
        location=Location(latitude=row["latitude"], longitude=row["longitude"]),
        bio=row["bio"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"])
    )


def get_all_users() -> List[User]:
    with get_db_connection() as conn:
        curs = conn.cursor()
        # ST_X extracts Longitude, ST_Y extracts Latitude from the SpatiaLite POINT
        curs.execute('''
            SELECT 
                id, first_name, last_name, date_of_birth, email, gender, looking_for, 
                ST_X(location) as longitude, ST_Y(location) as latitude, 
                bio, created_at, updated_at
            FROM users
        ''')
        rows = curs.fetchall()
        return [_row_to_user(dict(row)) for row in rows]


def get_user_by_id(user_id: uuid.UUID) -> Optional[User]:
    with get_db_connection() as conn:
        curs = conn.cursor()
        curs.execute('''
            SELECT 
                id, first_name, last_name, date_of_birth, email, gender, looking_for, 
                ST_X(location) as longitude, ST_Y(location) as latitude, 
                bio, created_at, updated_at
            FROM users WHERE id = ?
        ''', (str(user_id),))
        row = curs.fetchone()
        return _row_to_user(dict(row)) if row else None


def create_user(user: User) -> User:
    with get_db_connection() as conn:
        try:
            curs = conn.cursor()
            # MakePoint takes (longitude, latitude, SRID). SRID 4326 is standard GPS.
            curs.execute('''
                INSERT INTO users (id, first_name, last_name, date_of_birth, email, gender, looking_for, location, bio, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, MakePoint(?, ?, 4326), ?, ?, ?)
            ''', (
                str(user.id),
                user.first_name,
                user.last_name,
                user.date_of_birth.isoformat(),
                user.email,
                user.gender.value,
                user.looking_for.value,
                user.location.longitude,  # X
                user.location.latitude,   # Y
                user.bio,
                user.created_at.isoformat(),
                user.updated_at.isoformat()
            ))
            conn.commit()
            return user 
        except sqlite3.IntegrityError as e:
            # Handle unique constraint violations (e.g., duplicate email)
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"User with email {user.email} already exists.")
            else:
                raise

  
def update_user(user: User) -> User:
    """Updates an existing user. (Replaces both 'modify' and 'replace')."""
    with get_db_connection() as conn:
        curs = conn.cursor()
        curs.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, date_of_birth = ?, email = ?, 
                gender = ?, looking_for = ?, location = MakePoint(?, ?, 4326), 
                bio = ?, updated_at = ?
            WHERE id = ?
        ''', (
            user.first_name,
            user.last_name,
            user.date_of_birth.isoformat(),
            user.email,
            user.gender.value,
            user.looking_for.value,
            user.location.longitude,
            user.location.latitude,
            user.bio,
            user.updated_at.isoformat(),
            str(user.id)
        ))
        conn.commit()
        return user
    

def delete_user(user_id: uuid.UUID) -> bool:
    with get_db_connection() as conn:
        curs = conn.cursor()
        curs.execute("DELETE FROM users WHERE id = ?", (str(user_id),))
        conn.commit()
        return curs.rowcount > 0

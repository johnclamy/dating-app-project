import sqlite3
from backend.src.model.location import Location
from model.users import User


DB_NAME = "cupids_bow.db"


# Connect to your SQLite database
conn = sqlite3.connect(DB_NAME)

# Enable extension loading on the connection
conn.enable_load_extension(True)

# Load the SpatiaLite library
# (Linux usually automatically resolves 'mod_spatialite' if installed via apt)
# We will Load the exact file path found in Linux Mint 22
try:
    conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
    print("Extension loaded via direct path!")
except sqlite3.OperationalError:
    try:
        conn.load_extension("mod_spatialite")
        print("Extension loaded via system shortcut!")
    except sqlite3.OperationalError as e:
        print(f"Failed to load SpatiaLite extension: {e}")
        conn.close()
        raise

# Initialize spatial metadata tables
curs = conn.cursor()
curs.execute("SELECT InitSpatialMetaData(1);") # '1' accelerates initialization on modern SpatiaLite


def init():
    curs.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            gender TEXT NOT NULL,
            looking_for TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            bio TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')


def row_to_model(row: tuple) -> User:
    id,first_name, last_name, date_of_birth, email, gender, looking_for, latitude, longitude, bio, created_at, updated_at = row
    return User(
        id=id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        email=email,
        gender=gender,
        looking_for=looking_for,
        location=Location(latitude=latitude, longitude=longitude),
        bio=bio,
        created_at=created_at,
        updated_at=updated_at
    )


def model_to_dict(user: User) -> dict:
    return user.dict()


def get_user_by_id(user_id: str) -> User | None:
    curs.execute("SELECT * FROM users WHERE id = :user_id", {"user_id": user_id})
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    return None


def get_all_users() -> list[User]:
    curs.execute("SELECT * FROM users")
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create_user(user: User) -> User:
    user_dict = model_to_dict(user)
    curs.execute('''
        INSERT INTO users (id, first_name, last_name, date_of_birth, email, gender, looking_for, latitude, longitude, bio, created_at, updated_at)
        VALUES (:id, :first_name, :last_name, :date_of_birth, :email, :gender, :looking_for, :latitude, :longitude, :bio, :created_at, :updated_at)
    ''', user_dict)
    conn.commit()
    return user


def modify(user: User) -> User:
    user_dict = model_to_dict(user)
    curs.execute('''
        UPDATE users
        SET first_name = :first_name, last_name = :last_name, date_of_birth = :date_of_birth, email = :email, gender = :gender, looking_for = :looking_for, latitude = :latitude, longitude = :longitude, bio = :bio, updated_at = :updated_at
        WHERE id = :id
    ''', user_dict)
    conn.commit()
    return user


def replace(user: User) -> User:
    user_dict = model_to_dict(user)
    curs.execute('''
        UPDATE users
        SET first_name = :first_name, last_name = :last_name, date_of_birth = :date_of_birth, email = :email, gender = :gender, looking_for = :looking_for, latitude = :latitude, longitude = :longitude, bio = :bio, created_at = :created_at, updated_at = :updated_at
        WHERE id = :id
    ''', user_dict)
    conn.commit()
    return user


def delete_user(user_id: str) -> bool:
    curs.execute("DELETE FROM users WHERE id = :user_id", {"user_id": user_id})
    conn.commit()
    return curs.rowcount > 0


conn.close()

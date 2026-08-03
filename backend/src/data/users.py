import uuid
from model.location import Location
from model.users import User
from .init import conn, curs


if conn and curs:
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

    def get_user_by_id(user_id: uuid.UUID) -> User | None:
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

    def delete_user(user_id: uuid.UUID) -> bool:
        curs.execute("DELETE FROM users WHERE id = :user_id", {"user_id": user_id})
        conn.commit()
        return curs.rowcount > 0

    conn.close()

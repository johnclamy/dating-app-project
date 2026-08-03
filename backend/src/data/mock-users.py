# THIS FILE HAS BEEN RENAMED TO mock-users.py.
# IT WAS ORIGINALLY USED FOR NON DATABASE USE.
# IF YOU DO NOT NEED TO USE A DB, RENAME THIS
# FILE BACK TO users.py AND ARCHIVE THE OTHER
# users.py FILE THAT USES A SQLITE DB.


import uuid
from datetime import date, datetime, timezone
from model.users import User
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location


# Data list used here for testing. Will be replaced with a database connection later.
_users = [
    User(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174003"),
        first_name="Diana",
        last_name="Evans",
        date_of_birth=date(1998, 7, 20),  # Age 28
        email="diana.e@example.com",
        gender=Gender.FEMALE,
        looking_for=LookingFor.RELATIONSHIP,
        location=Location(latitude=-33.8688, longitude=151.2093), # Sydney
        bio="Beach lover and amateur photographer. Looking for someone to explore the coast with.",
        created_at=datetime(2026, 7, 28, 18, 45, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 7, 28, 18, 45, 0, tzinfo=timezone.utc)
    ),
    User(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174002"),
        first_name="Charlie",
        last_name="Davis",
        date_of_birth=date(2002, 1, 15),  # Age 24
        email="charlie.d@example.com",
        gender=Gender.NON_BINARY,
        looking_for=LookingFor.FRIENDSHIP,
        location=Location(latitude=35.6895, longitude=139.6917), # Tokyo
        bio=None,  # Bio is optional
        created_at=datetime(2026, 8, 1, 8, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 8, 1, 8, 0, 0, tzinfo=timezone.utc)
    ),
    User(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174001"),
        first_name="Bob",
        last_name="Johnson",
        date_of_birth=date(1990, 11, 30),  # Age 35
        email="bob.j@example.com",
        gender=Gender.MALE,
        looking_for=LookingFor.CASUAL,
        location=Location(latitude=51.5074, longitude=-0.1278), # London
        bio="Musician and foodie. Let's grab a pint.",
        created_at=datetime(2026, 7, 20, 14, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 7, 22, 9, 15, 0, tzinfo=timezone.utc) # Updated profile later
    ),
    User(
        id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date(1995, 4, 12),  # Age 31
        email="alice.smith@example.com",
        gender=Gender.FEMALE,
        looking_for=LookingFor.RELATIONSHIP,
        location=Location(latitude=40.7128, longitude=-74.0060), # New York
        bio="Love hiking, weekend coffee runs, and trying new restaurants.",
        created_at=datetime(2026, 7, 15, 10, 30, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 7, 15, 10, 30, 0, tzinfo=timezone.utc)
    )
]


# CRUD operations for users

def get_all() -> list[User]:
    """Retrieve all users."""
    return _users


def get_by_id(user_id: uuid.UUID) -> User | None:
    """Retrieve a user by ID."""
    for user in _users:
        if user.id == user_id:
            return user
    return None


def create(user: User) -> User:
    """Create a new user."""
    _users.append(user)
    return user


def modify(user_id: uuid.UUID, updated_user: User) -> User | None:
    """Partially modify a user."""
    for index, user in enumerate(_users):
        if user.id == user_id:
            _users[index] = updated_user
            return updated_user
    return None


def replace(user_id: uuid.UUID, new_user: User) -> User | None:
    """Completely replace a user."""
    for index, user in enumerate(_users):
        if user.id == user_id:
            _users[index] = new_user
            return new_user
    return None


def delete(user_id: uuid.UUID) -> bool:
    """Delete a user."""
    for index, user in enumerate(_users):
        if user.id == user_id:
            del _users[index]
            return True
    return False
    

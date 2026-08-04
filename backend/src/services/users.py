from model.users import User
import data.users as data
import uuid


def get_all() -> list[User]:
    """Retrieve all users."""
    return data.get_all_users()


def get_by_id(user_id: uuid.UUID) -> User | None:
    """Retrieve a user by ID."""
    return data.get_user_by_id(user_id)


def create(user: User) -> User:
    """Create a new user."""
    return data.create_user(user)


def update(user: User) -> User:
    """Update an existing user."""
    return data.update_user(user)


def delete(user_id: uuid.UUID) -> bool:
    """Delete a user."""
    return data.delete_user(user_id)

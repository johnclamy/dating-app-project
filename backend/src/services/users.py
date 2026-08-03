from model.users import User
import data.users as data
import uuid


def get_all() -> list[User]:
    """Retrieve all users."""
    return data.get_all()


def get_by_id(user_id: uuid.UUID) -> User | None:
    """Retrieve a user by ID."""
    return data.get_by_id(user_id)


def create(user: User) -> User:
    """Create a new user."""
    return data.create(user)


def replace(user_id: uuid.UUID, new_user: User) -> User | None:
    """Completely replace a user."""
    return data.replace(user_id, new_user)


def modify(user_id: uuid.UUID, updated_user: User) -> User | None:
    """Partially modify a user."""
    return data.modify(user_id, updated_user)


def delete(user_id: uuid.UUID) -> bool:
    """Delete a user."""
    return data.delete(user_id)

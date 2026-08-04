from validator.user import validate_user
from model.users import User
import data.users as data
import logging
import uuid


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all() -> list[User] | list[None] | None:
    """Retrieve all users."""
    logger.info("Retrieving all users.")

    try:
        users = data.get_all_users()
        if users is not None:            
            logger.info(f"Retrieved {len(users)} users.")
        else:
            logger.warning("No users found.")
        return users
    
    except Exception as e:
        logger.error(f"Error occurred while retrieving all users. Error: {e}")
        return None


def get_by_id(user_id: uuid.UUID) -> User | None:
    """Retrieve a user by ID."""
    logger.info(f"Retrieving user with ID: {user_id}")

    try: 
        user = data.get_user_by_id(user_id)

        if user:
            logger.info(f"User found: {user}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return user
    
    except Exception as e:
        logger.error(f"Error occurred while retrieving user with ID: {user_id}. Error: {e}")
        return None


def create(user: User) -> User:
    """Create a new user."""
    logger.info(f"Creating user: {user}")

    try:
        validate_user(user)
        created_user = data.create_user(user)
        logger.info(f"User created: {created_user}")
        return created_user
    except ValueError as ve:
        logger.error(f"Value error occurred while creating user. Error: {ve}")
        raise
    except Exception as e:
        logger.error(f"Error occurred while creating user. Error: {e}")
        raise


def update(user_id: uuid.UUID, user: User) -> User | None:
    """Update an existing user."""
    logger.info(f"Updating user with ID: {user_id}")

    try:
        validate_user(user)
        updated_user = data.update_user(user)
        if updated_user:
            logger.info(f"User updated: {updated_user}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return updated_user
    
    except ValueError as ve:
        logger.error(f"Value error occurred while updating user with ID: {user_id}. Error: {ve}")
        return None
    except Exception as e:
        logger.error(f"Error occurred while updating user with ID: {user_id}. Error: {e}")
        return None


def delete(user_id: uuid.UUID) -> bool:
    """Delete a user."""
    logger.info(f"Deleting user with ID: {user_id}")
    try:
        deleted = data.delete_user(user_id)
        if deleted:
            logger.info(f"User deleted: {user_id}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return deleted
    except Exception as e:
        logger.error(f"Error occurred while deleting user with ID: {user_id}. Error: {e}")
        return False

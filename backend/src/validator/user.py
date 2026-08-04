from datetime import date, datetime
from model.users import User


def validate_user(user: User) -> None:
    """Validate user data before operations."""
    if user.date_of_birth:
        today = date.today()
        age = today.year - user.date_of_birth.year - ((today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day))
        if age < 18:
            raise ValueError("User must be at least 18 years old.")
        if user.date_of_birth > today:
            raise ValueError("Date of birth cannot be in the future.")

    if user.email and ("@" not in user.email or "." not in user.email.split("@")[-1]):
        raise ValueError("Invalid email format.")

    if user.first_name and not user.first_name.isalpha():
        raise ValueError("First name must only contain alphabetic characters.")

    if user.last_name and not user.last_name.isalpha():
        raise ValueError("Last name must only contain alphabetic characters.")

    if user.bio and len(user.bio) > 500:
        raise ValueError("Bio must be 500 characters or fewer.")

    if user.updated_at and user.created_at and user.updated_at < user.created_at:
        raise ValueError("Updated at timestamp cannot be before created at timestamp.")

    if user.updated_at and user.updated_at > datetime.now():
        raise ValueError("Updated at timestamp cannot be in the future.")

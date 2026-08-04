from pydantic import field_validator, ValidationInfo
from datetime import date, datetime


@field_validator("date_of_birth")
@classmethod
def validate_age(cls, value: date) -> date:
    """Ensures the user is at least 18 years old (standard for dating apps)."""
    today = date.today()

    # Calculate age
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValueError("User must be at least 18 years old.")
    if value > today:
            raise ValueError("Date of birth cannot be in the future.")
    return value


@field_validator("email")
@classmethod
def validate_email(cls, value: str) -> str:
    """Ensures the email is in a valid format."""
    if "@" not in value or "." not in value.split("@")[-1]:
        raise ValueError("Invalid email format.")
    return value


@field_validator("first_name", "last_name")
@classmethod
def validate_name(cls, value: str) -> str:
    """Ensures names are not empty and do not contain numbers or special characters."""
    if not value.isalpha():
        raise ValueError("Names must only contain alphabetic characters.")
    return value


@field_validator("bio")
@classmethod
def validate_bio(cls, value: str) -> str:
    """Ensures the bio is not too long."""
    if value and len(value) > 500:
        raise ValueError("Bio must be 500 characters or fewer.")
    return value


@field_validator("updated_at")
@classmethod
def validate_updated_at(cls, value: datetime, info: ValidationInfo) -> datetime:
    """Ensures updated_at is never before created_at."""
    created_at = info.data.get("created_at") if info and getattr(info, "data", None) is not None else None
    if created_at and value < created_at:
        raise ValueError("Updated at timestamp cannot be before created at timestamp.")
    
    """Ensures the updated_at timestamp is not in the future."""
    if value > datetime.now():
        raise ValueError("Updated at timestamp cannot be in the future.")
    return value

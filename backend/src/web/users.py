import uuid
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr, Field, field_validator
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, select
# --- Move get_session to dependencies.py to avoid circular imports with main.py ---
from dependencies import get_session
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location
from model.users import User


router = APIRouter()


# ---------------------------------------------------------------------------
# API Request/Response Schemas
# ---------------------------------------------------------------------------

class UserCreate(SQLModel):
    """Request body for creating a new user."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date = Field(
        ..., description="Must be at least 18 years old"
    )
    email: EmailStr = Field(..., max_length=255)
    gender: Gender
    looking_for: LookingFor
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Y coordinate")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="X coordinate")
    bio: Optional[str] = Field(default=None, max_length=500)
    # NOTE: You must add `password_hash` to your User model.
    # This field is write-only and never returned in responses.
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("date_of_birth")
    @classmethod
    def must_be_adult(cls, v: date) -> date:
        """Ensure the user is at least 18 years old."""
        # Approximate 18 years; leap-day safe
        age_cutoff = date.today().replace(year=date.today().year - 18)
        if v > age_cutoff:
            raise ValueError("Must be at least 18 years old")
        return v


class UserRead(SQLModel):
    """Response body for reading a user."""
    id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    gender: Gender
    looking_for: LookingFor
    # Uses the @property location on the User model
    location: Location
    bio: Optional[str] = None
    created_at: Optional[date] = None  # type: ignore[assignment]


class UserUpdate(SQLModel):
    """Request body for partial updates (PATCH)."""
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = Field(
        default=None, description="Must be at least 18 years old"
    )
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    gender: Optional[Gender] = None
    looking_for: Optional[LookingFor] = None
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    bio: Optional[str] = Field(default=None, max_length=500)

    @field_validator("date_of_birth")
    @classmethod
    def must_be_adult(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v
        age_cutoff = date.today().replace(year=date.today().year - 18)
        if v > age_cutoff:
            raise ValueError("Must be at least 18 years old")
        return v


# ---------------------------------------------------------------------------
# CRUD Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user profile",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_session),
) -> User:
    """Create a new user profile after checking email uniqueness."""
    # Build the DB model from the request.
    # We pop `password` because the User table stores `password_hash`, not plain text.
    user_data = user_in.model_dump(exclude={"password"})
    db_user = User.model_validate(user_data)

    # TODO: Hash the password before storing.
    # Example: db_user.password_hash = hash_password(user_in.password)
    # For now, this is a placeholder to remind you to wire in your auth layer.
    # db_user.password_hash = "placeholder"

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return db_user


@router.get(
    "/",
    response_model=List[UserRead],
    summary="List user profiles",
)
def read_users(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return (hard cap: 500)"),
    db: Session = Depends(get_session),
) -> List[User]:
    """Retrieve a paginated list of users."""
    users = db.exec(select(User).offset(offset).limit(limit)).all()
    return users # type: ignore


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get a single user profile",
)
def read_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_session),
) -> User:
    """Get a single user profile by UUID."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Update user profile",
)
def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_session),
) -> User:
    """Partially update a user profile."""
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_in.model_dump(exclude_unset=True)

    # Prevent email collisions on update
    new_email = update_data.get("email")
    if new_email and new_email != db_user.email:
        existing = db.exec(select(User).where(User.email == new_email)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    for key, value in update_data.items():
        setattr(db_user, key, value)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return db_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user profile",
)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_session),
) -> None:
    """Delete a user profile permanently."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()
    return None
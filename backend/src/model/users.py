import uuid
from datetime import date, datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location


# --- Main User Model ---
class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Primary key")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date = Field(..., description="Must be at least 18 years old")
    email: EmailStr = Field(..., max_length=255)
    gender: Gender
    looking_for: LookingFor
    # SpatiaLite will store this as a POINT geometry, but we keep it as lat/lon in Pydantic
    location: Location
    bio: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

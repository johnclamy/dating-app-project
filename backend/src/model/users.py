import uuid
from datetime import date, datetime, timedelta
from typing import ClassVar, Optional
from pydantic import EmailStr, field_validator
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    String,
    Uuid,
)
from sqlmodel import Field, SQLModel
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location
from helper.sql_alchm_enum import _enum_column
from helper.date_time import utcnow


@field_validator("date_of_birth")
@classmethod
def must_be_18(cls, v: date) -> date:
    if v > date.today() - timedelta(days=18*365):
        raise ValueError("Must be at least 18 years old")
    return v


# --- Database model ---
class User(SQLModel, table=True):
    __tablename__: ClassVar[str] = "users" # pyright: ignore[reportIncompatibleVariableOverride]

    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name="ck_users_latitude_range",
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name="ck_users_longitude_range",
        ),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_type=Uuid,
        description="Primary key",
    )

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    date_of_birth: date = Field(
        ...,
        description="Must be at least 18 years old",
    )

    email: EmailStr = Field(
        ...,
        max_length=255,
        sa_column=Column(
            String(255),
            unique=True,
            index=True,
            nullable=False,
        ),
    )

    gender: Gender = Field(
        sa_column=Column(
            _enum_column(Gender),
            nullable=False,
        ),
    )

    looking_for: LookingFor = Field(
        sa_column=Column(
            _enum_column(LookingFor),
            nullable=False,
        ),
    )

    # Store the point as scalar columns.
    # This is the SQLModel-friendly bridge to SpatiaLite.
    latitude: float = Field(
        ...,
        sa_type=Float,
        ge=-90.0,
        le=90.0,
        description="Y coordinate",
    )

    longitude: float = Field(
        ...,
        sa_type=Float,
        ge=-180.0,
        le=180.0,
        description="X coordinate",
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utcnow,
        ),
    )

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utcnow,
            onupdate=utcnow,
        ),
    )

    @property
    def location(self) -> Location:
        """
        API-facing representation.

        This lets UserRead serialize the user as:

            {
                "location": {
                    "latitude": ...,
                    "longitude": ...
                }
            }
        """
        return Location(
            latitude=self.latitude,
            longitude=self.longitude,
        )

    @property
    def wkt_point(self) -> str:
        """
        Useful if you later store a true SpatiaLite POINT geometry.

        SpatiaLite POINT order is:

            POINT(X Y) = POINT(longitude latitude)
        """
        return f"POINT({self.longitude} {self.latitude})"
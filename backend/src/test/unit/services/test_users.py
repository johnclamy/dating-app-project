import uuid
from datetime import date, datetime, timezone
from model.users import User
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location
from services.users import get_all, get_by_id, create, replace, modify, delete


sample = User(
    id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
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


def test_create():
    resp = create(sample)
    assert resp == sample


def test_get_exists():
    resp = get_by_id(uuid.UUID("12345678-1234-5678-1234-567812345678"))
    assert resp == sample


def test_get_not_exists():
    resp = get_by_id(uuid.UUID("00000000-0000-0000-0000-000000000000"))
    assert resp is None

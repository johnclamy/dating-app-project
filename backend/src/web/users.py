import hashlib
import secrets
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, select

from ..model.users import User, UserCreate, UserRead, UserUpdate, utcnow
from .dependencies import SessionDep, UserDep

router = APIRouter(prefix="/users", tags=["users"])

PBKDF2_ITERATIONS = 200_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        PBKDF2_ITERATIONS,
    ).hex()

    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${digest}"


def username_exists(
    session: Session,
    username: str,
    exclude_user_id: UUID | None = None,
) -> bool:
    stmt = select(User).where(User.username == username)

    if exclude_user_id is not None:
        stmt = stmt.where(User.id != exclude_user_id)

    return session.exec(stmt).first() is not None


def email_exists(
    session: Session,
    email: str,
    exclude_user_id: UUID | None = None,
) -> bool:
    stmt = select(User).where(User.email == email)

    if exclude_user_id is not None:
        stmt = stmt.where(User.id != exclude_user_id)

    return session.exec(stmt).first() is not None


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(payload: UserCreate, session: SessionDep) -> User:
    if username_exists(session, payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    if email_exists(session, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("", response_model=list[UserRead])
def list_users(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
) -> list[User]:
    stmt = select(User).offset(offset).limit(limit)
    users = session.exec(stmt).all()
    return list(users)


@router.get("/{user_id}", response_model=UserRead)
def read_user(user: UserDep) -> User:
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    payload: UserUpdate,
    user: UserDep,
    session: SessionDep,
) -> User:
    data = payload.model_dump(exclude_unset=True)

    password = data.pop("password", None)
    username = data.get("username")
    email = data.get("email")

    if username is not None and username_exists(
        session,
        username,
        exclude_user_id=user.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    if email is not None and email_exists(
        session,
        email,
        exclude_user_id=user.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    for field_name, value in data.items():
        setattr(user, field_name, value)

    if password is not None:
        user.hashed_password = hash_password(password)

    user.updated_at = utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user: UserDep, session: SessionDep) -> None:
    session.delete(user)
    session.commit()
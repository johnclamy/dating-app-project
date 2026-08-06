from collections.abc import Generator
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine

from ..model.users import User

BACKEND_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BACKEND_DIR / "db"
DB_FILE = DB_DIR / "cupids_bow.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_user(user_id: UUID, session: SessionDep) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


UserDep = Annotated[User, Depends(get_user)]

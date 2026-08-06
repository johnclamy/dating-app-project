from typing import Generator
from sqlmodel import Session
from backend.src.main import engine


def get_session() -> Generator[Session, None, None]:
    """Dependency to provide a DB session per request."""
    with Session(engine) as session:
        yield session

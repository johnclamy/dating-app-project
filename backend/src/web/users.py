from fastapi import APIRouter
from model.users import User
import services.users as service
import uuid


router = APIRouter(prefix="/users")


@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{user_id}")
def get_by_id(user_id: str) -> User | None:
    return service.get_by_id(uuid.UUID(user_id))


@router.post("/")
def create(user: User) -> User:
    return service.create(user)


@router.put("/{user_id}")
def update(user_id: str, user: User) -> User | None:
    return service.update(uuid.UUID(user_id), user)


@router.delete("/{user_id}")
def delete(user_id: str) -> bool:
    return service.delete(uuid.UUID(user_id))

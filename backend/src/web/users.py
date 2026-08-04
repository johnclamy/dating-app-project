from fastapi import APIRouter, HTTPException, status
from model.users import User
import services.users as service
import uuid


router = APIRouter(prefix="/users")


@router.get("/")
def get_all() -> list[User] | list[None] | None:
    return service.get_all()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_by_id(user_id: str) -> User | None:
    '''Get user by ID'''
    try:
        user = service.get_by_id(uuid.UUID(user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    '''Create a new user'''
    try:
        created_user = service.create(user)
        return created_user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update(user_id: str, user: User) -> User | None:
    return service.update(uuid.UUID(user_id), user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete(user_id: str) -> bool:
    return service.delete(uuid.UUID(user_id))

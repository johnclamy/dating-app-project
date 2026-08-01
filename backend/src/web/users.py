from fastapi import APIRouter


router = APIRouter(prefix="/users")


@router.get("/")
def read_root():
    return {"Users": "Root users endpoint"}

import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine


# Path to backend/db/cupids_bow.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "cupids_bow.db")


# Ensure the backend/db directory exists
os.makedirs(DB_DIR, exist_ok=True)


DATABASE_URL = f"sqlite:///{DB_PATH}"


# SQLite requires connect_args for multithreading in FastAPI
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB and tables on startup
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Cupid's Bow API", lifespan=lifespan)


# Import and include the user CRUD router
from web.users import router as user_router
app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Welcome to Cupid's Bow API"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

# import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .web.dependencies import create_db_and_tables
from .web.users import router as users_router

VERSION = "0.2.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Cupid's Bow",
    version=VERSION,
    lifespan=lifespan,
)

app.include_router(users_router, prefix="/api/v1")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "version": VERSION,
    }


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )

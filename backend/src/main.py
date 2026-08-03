import uvicorn
from fastapi import FastAPI
from data.init import init_spatialite_once
from web.users import router as users_router


app = FastAPI()


# Initialize the database schema/metadata exactly once at startup
init_spatialite_once()


app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

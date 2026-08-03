import uvicorn
from fastapi import FastAPI
from data.init import init_spatialite_once
from data.users import init_db_schema
from web.users import router as users_router


app = FastAPI()


# Initialize the database schema/metadata exactly once at startup
# inside your lifespan or startup event:
init_spatialite_once()
init_db_schema()


app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

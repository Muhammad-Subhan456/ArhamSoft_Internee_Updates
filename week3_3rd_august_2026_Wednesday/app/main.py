from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.database import Base, engine
from app.models import Category, Task
from app.routers.v1_tasks import router


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task API with SQLAlchemy",
    version="1.0.0",
)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["Version 1"],
)
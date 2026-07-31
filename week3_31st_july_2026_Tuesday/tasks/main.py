from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from routers.v1_tasks import router as v1_router
from database import create_tables

app = FastAPI()
create_tables()

app.include_router(
    v1_router,
    prefix="/api/v1",
    tags=["Version 1"]
)

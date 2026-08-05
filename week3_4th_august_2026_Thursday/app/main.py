from fastapi import FastAPI

from app.database import Base, engine
from app.models import Category, Note, User
from app.routers.auth import router as auth_router
from app.routers.notes import router as notes_router
from app.routers.admin import router as admin_router
from app.routers.categories import router as categories_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="Notes API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(admin_router)
app.include_router(categories_router)


    
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend",
)

@app.get("/")
def home():
    return FileResponse("frontend/index.html")
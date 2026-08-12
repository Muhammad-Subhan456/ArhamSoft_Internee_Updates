import os
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.routers.notes import router as notes_router
from app.routers.admin import router as admin_router
from app.routers.categories import router as categories_router

app = FastAPI(
    title="Notes API",
    version="1.0.0",
)

cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

extra_origins = os.getenv("CORS_ORIGINS", "")
if extra_origins.strip():
    cors_origins.extend(
        origin.strip()
        for origin in extra_origins.split(",")
        if origin.strip()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(admin_router)
app.include_router(categories_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Ensures JSON 500 responses still pass through CORSMiddleware.
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/")
def home():
    return {
        "message": "Notes API is running",
        "docs": "/docs",
    }

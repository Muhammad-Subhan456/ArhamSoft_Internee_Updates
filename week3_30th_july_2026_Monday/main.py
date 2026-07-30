from fastapi import FastAPI
from routers.v1_tasks import router as v1_router
from routers.v2_tasks import router as v2_router
from routers.demo import router as demo_router
from routers.sync_async import router as sync_async_router

app = FastAPI()

# If v2 needed to rename a field without breaking existing v1 clients, 
# we would keep the existing /api/v1 endpoints unchanged and introduce the renamed field
# in a new /api/v2 version so existing clients continue to work while new clients migrate 
# to the updated API.

app.include_router(
    v1_router,
    prefix="/api/v1",
    tags=["Version 1"]
)

app.include_router(
    v2_router,
    prefix="/api/v2",
    tags=["Version 2"],
)

app.include_router(
    demo_router,
    prefix="/api",
    tags=["Async Demo"],
)

app.include_router(
    sync_async_router,
    prefix="/demo",
    tags=["Sync vs Async"],
)
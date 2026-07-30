from fastapi import APIRouter
import asyncio
import time

router = APIRouter()


@router.get("/sync")
def sync_endpoint():
    time.sleep(2)

    return {
        "type": "sync",
        "message": "Finished after 2 seconds"
    }


@router.get("/async")
async def async_endpoint():
    await asyncio.sleep(2)

    return {
        "type": "async",
        "message": "Finished after 2 seconds"
    }


@router.get("/instant")
async def instant():
    return {
        "message": "Immediate response"
    }
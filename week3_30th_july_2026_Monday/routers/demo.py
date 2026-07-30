from fastapi import APIRouter
import asyncio
from datetime import datetime

router = APIRouter()


@router.get("/slow")
async def slow_endpoint():
    start = datetime.now()

    await asyncio.sleep(2)

    end = datetime.now()

    return {
        "message": "Finished processing",
        "start": start.strftime("%H:%M:%S"),
        "end": end.strftime("%H:%M:%S"),
    }
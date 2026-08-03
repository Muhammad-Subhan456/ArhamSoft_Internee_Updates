import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")


async def verify_api_key(
    x_api_key: str = Header(...)
):
    print("Header:", x_api_key)
    print("Env:", API_KEY)

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )
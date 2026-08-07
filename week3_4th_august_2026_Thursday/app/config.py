import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


class Settings:
    DATABASE_URL: str = os.environ["DATABASE_URL"]

    SECRET_KEY: str = os.environ["SECRET_KEY"]

    ALGORITHM: str = os.environ["ALGORITHM"]

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
    )


settings = Settings()
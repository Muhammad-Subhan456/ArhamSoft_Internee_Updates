import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Prefer process env (Docker Compose), then project-root/.env, then backend/.env.
env_path = PROJECT_ROOT / ".env"
if not env_path.is_file():
    env_path = BACKEND_DIR / ".env"

# Do not override variables already set by Docker Compose / the shell.
load_dotenv(env_path, override=False)


class Settings:
    DATABASE_URL: str = os.environ["DATABASE_URL"]

    SECRET_KEY: str = os.environ["SECRET_KEY"]

    ALGORITHM: str = os.environ["ALGORITHM"]

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
    )


settings = Settings()

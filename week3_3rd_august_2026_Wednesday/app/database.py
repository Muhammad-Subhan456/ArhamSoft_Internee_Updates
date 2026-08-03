from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "sqlite:///tasks.db"


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)

# Session Factory
#
# A new Session will be created for every request.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


#
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass




def get_db() -> Generator[Session, None, None]:
    """
    Creates a database session for each request.

    The session is automatically closed after the request
    finishes, even if an exception occurs.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
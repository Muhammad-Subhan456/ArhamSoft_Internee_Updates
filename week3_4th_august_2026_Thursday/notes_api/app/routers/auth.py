from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return auth_service.register_user(db, user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    return auth_service.login_user(db, credentials)
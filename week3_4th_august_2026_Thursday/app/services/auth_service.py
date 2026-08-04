from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User
from app.schemas import Token, UserLogin, UserRegister
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserRegister,
    ) -> User:

        existing_user = db.scalar(
            select(User).where(
                or_(
                    User.email == user_data.email,
                    User.username == user_data.username,
                )
            )
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already exists",
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role="user",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login_user(
        db: Session,
        credentials: UserLogin,
    ) -> Token:
    

        user = db.scalar(
            select(User).where(
                User.email == credentials.email
            )
        )

        if (
            user is None
            or not verify_password(
                credentials.password,
                user.hashed_password,
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "role": user.role,
            },
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )


auth_service = AuthService()
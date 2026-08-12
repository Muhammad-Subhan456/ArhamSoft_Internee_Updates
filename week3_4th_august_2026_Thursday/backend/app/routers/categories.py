from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(db, category, current_user)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_categories(db, current_user)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def read_one(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_category(db, category_id, current_user)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_category(
        db,
        category_id,
        category,
        current_user,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_category(
        db,
        category_id,
        current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

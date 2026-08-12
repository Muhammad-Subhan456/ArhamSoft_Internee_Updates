from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, User
from app.schemas import CategoryCreate, CategoryUpdate


def create_category(
    db: Session,
    category: CategoryCreate,
    current_user: User,
):
    existing = db.scalar(
        select(Category).where(
            Category.owner_id == current_user.id,
            Category.name == category.name,
        )
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )

    db_category = Category(
        name=category.name,
        owner_id=current_user.id,
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def get_categories(db: Session, current_user: User):
    return list(
        db.scalars(
            select(Category).where(Category.owner_id == current_user.id)
        )
    )


def get_category(
    db: Session,
    category_id: int,
    current_user: User,
):
    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
            Category.owner_id == current_user.id,
        )
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User,
):
    category = get_category(db, category_id, current_user)

    duplicate = db.scalar(
        select(Category).where(
            Category.owner_id == current_user.id,
            Category.name == category_data.name,
            Category.id != category_id,
        )
    )

    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int,
    current_user: User,
):
    category = get_category(db, category_id, current_user)

    db.delete(category)
    db.commit()

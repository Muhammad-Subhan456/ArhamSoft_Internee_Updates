from app.security import verify_api_key
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Category, Task
from app.schemas import (
    CategoryCreate,
    CategoryResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter()



@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    existing_category = db.scalar(
        select(Category).where(Category.name == category.name)
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
        )

    new_category = Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
)
async def get_categories(
    db: Session = Depends(get_db),
):
    categories = db.scalars(
        select(Category)
    ).all()

    return categories


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
)
async def get_tasks(
    db: Session = Depends(get_db),
):
    tasks = db.scalars(
        select(Task)
        .options(joinedload(Task.category))
    ).all()

    return tasks


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = db.scalar(
        select(Task)
        .options(joinedload(Task.category))
        .where(Task.id == task_id)
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    if task.category_id is not None:

        category = db.get(Category, task.category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    new_task = Task(
        title=task.title,
        completed=task.completed,
        category_id=task.category_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    existing_task = db.get(Task, task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.category_id is not None:

        category = db.get(Category, task.category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    existing_task.title = task.title
    existing_task.completed = task.completed
    existing_task.category_id = task.category_id

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
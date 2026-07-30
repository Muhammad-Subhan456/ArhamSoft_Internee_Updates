from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

router = APIRouter()


class TaskV2(BaseModel):
    name: str
    completed: bool = False


tasks = [
    {
        "id": 1,
        "name": "Learn FastAPI",
        "completed": False
    }
]


@router.get("/tasks")
async def get_tasks():
    return tasks


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(404, "Task not found")


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED
)
async def create_task(task: TaskV2):

    new_task = {
        "id": len(tasks) + 1,
        "name": task.name,
        "completed": task.completed,
    }

    tasks.append(new_task)

    return new_task


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, updated: TaskV2):

    for task in tasks:
        if task["id"] == task_id:
            task["name"] = updated.name
            task["completed"] = updated.completed
            return task

    raise HTTPException(404, "Task not found")


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    raise HTTPException(404, "Task not found")
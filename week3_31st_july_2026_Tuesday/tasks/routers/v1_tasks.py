from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import BaseModel
from database import get_connection
from security import verify_api_key

router = APIRouter()

class Task(BaseModel):
    title: str
    completed: bool = False

@router.get("/tasks")
async def get_tasks():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    ).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(404, "Task not found")

    return dict(row)


@router.post(
    "/tasks",
    status_code=201
)
async def create_task(task: Task, _:None = Depends(verify_api_key)):

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO tasks(title, completed)
        VALUES(?,?)
        """,
        (
            task.title,
            task.completed,
        )
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return {
        "id": new_id,
        **task.model_dump()
    }
    
    
@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task: Task, _:None = Depends(verify_api_key)
):

    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE tasks
        SET title=?,
            completed=?
        WHERE id=?
        """,
        (
            task.title,
            task.completed,
            task_id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            404,
            "Task not found"
        )

    conn.close()

    return {
        "id": task_id,
        **task.model_dump()
    }
    
@router.delete(
    "/tasks/{task_id}",
    status_code=204
)
async def delete_task(task_id: int, _:None = Depends(verify_api_key)):

    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE
        FROM tasks
        WHERE id=?
        """,
        (task_id,)
    )

    conn.commit()

    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            404,
            "Task not found"
        )
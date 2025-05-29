from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models.task import Task, TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=list[TaskPublic])
def get_tasks(session: SessionDep):
    return session.exec(select(Task).order_by(-Task.id)).all()


@router.post("/tasks", response_model=TaskPublic, status_code=201)
def create_task(task: TaskCreate, session: SessionDep):
    task = Task.model_validate(task)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={404: {"description": "Task not found"}},
)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={404: {"description": "Task not found"}},
)
def update_task(task_id: int, task: TaskUpdate, session: SessionDep):
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)

    session.add(task_db)
    session.commit()
    session.refresh(task_db)

    return task_db


@router.delete("/tasks/{task_id}", responses={404: {"description": "Task not found"}})
def delete_task(task_id: int, session: SessionDep):
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task_db)
    session.commit()

    return {"message": "Task deleted successfully"}

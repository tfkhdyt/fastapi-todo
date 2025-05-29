from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.internal.db import SessionDep
from app.internal.security import CurrentUserDep
from app.models.task import Task, TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(tags=["tasks"])


def get_task_owner(
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this task"
        )
    return task


TaskOwnerDep = Annotated[Task, Depends(get_task_owner)]


@router.get("/tasks", response_model=list[TaskPublic])
def get_all_tasks(session: SessionDep, current_user: CurrentUserDep):
    return current_user.tasks


@router.post("/tasks", response_model=TaskPublic, status_code=201)
def create_task(payload: TaskCreate, session: SessionDep, current_user: CurrentUserDep):
    task_db = Task(**payload.model_dump(), user_id=current_user.id)

    session.add(task_db)
    session.commit()
    session.refresh(task_db)

    return task_db


@router.get(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
)
def get_task_by_id(task_owner: TaskOwnerDep):
    return task_owner


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
)
def update_task(task: TaskOwnerDep, payload: TaskUpdate, session: SessionDep):
    task_data = payload.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_data)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete(
    "/tasks/{task_id}",
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
)
def delete_task(task: TaskOwnerDep, session: SessionDep):
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}

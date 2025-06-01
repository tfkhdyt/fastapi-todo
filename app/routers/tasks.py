import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import desc, select

from app.internal.core.db import SessionDep
from app.internal.core.security import CurrentUserDep
from app.internal.models.task import Task, TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(tags=["tasks"])
logger = logging.getLogger(__name__)


async def get_task_owner(
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    task = await session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id} for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        logger.warning(
            f"User {current_user.username} attempted to access unowned task {task_id}"
        )
        raise HTTPException(
            status_code=403, detail="You are not the owner of this task"
        )
    return task


TaskOwnerDep = Annotated[Task, Depends(get_task_owner)]


@router.get("/tasks", response_model=list[TaskPublic])
async def get_all_tasks(current_user: CurrentUserDep, session: SessionDep):
    result = await session.exec(
        select(Task).where(Task.user_id == current_user.id).order_by(desc(Task.id))
    )
    tasks = result.all()
    return tasks


@router.post("/tasks", response_model=TaskPublic, status_code=201)
async def create_task(
    payload: TaskCreate, current_user: CurrentUserDep, session: SessionDep
):
    task_db = Task(
        title=payload.title,
        description=payload.description,
        user_id=current_user.id,
    )

    session.add(task_db)
    await session.commit()
    await session.refresh(task_db)

    return task_db


@router.get(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
)
async def get_task_by_id(task_owner: TaskOwnerDep):
    return task_owner


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
)
async def update_task(
    task: TaskOwnerDep,
    payload: TaskUpdate,
    session: SessionDep,
):
    task_data = payload.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_data)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.delete(
    "/tasks/{task_id}",
    responses={
        404: {"description": "Task not found"},
        403: {"description": "You are not the owner of this task"},
    },
    status_code=204,
)
async def delete_task(task: TaskOwnerDep, session: SessionDep):
    await session.delete(task)
    await session.commit()

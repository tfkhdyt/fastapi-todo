from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from app.internal.validators import (
    validate_task_description,
    validate_task_title,
)

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .user import User


# Base class with common fields
class TaskBase(SQLModel):
    title: str = Field(
        index=True,
        min_length=1,
        max_length=200,
        description="Task title must be 1-200 characters long",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description must not exceed 1000 characters",
    )
    done: bool = Field(default=False)

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        validated = validate_task_title(v)
        if validated is None:
            raise ValueError("Task title cannot be None")
        return validated

    @field_validator("description")
    @classmethod
    def validate_description_field(cls, v: str | None) -> str | None:
        return validate_task_description(v)


# Table model
class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    # Use string forward reference
    user: "User" = Relationship(back_populates="tasks")


# Public schema (what gets returned to clients)
class TaskPublic(TaskBase):
    id: int


# Create schema (for creating new tasks)
class TaskCreate(SQLModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title must be 1-200 characters long",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description must not exceed 1000 characters",
    )

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        validated = validate_task_title(v)
        if validated is None:
            raise ValueError("Task title cannot be None")
        return validated

    @field_validator("description")
    @classmethod
    def validate_description_field(cls, v: str | None) -> str | None:
        return validate_task_description(v)


# Update schema (for updating existing tasks)
class TaskUpdate(SQLModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title must be 1-200 characters long",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description must not exceed 1000 characters",
    )
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str | None) -> str | None:
        return validate_task_title(v)

    @field_validator("description")
    @classmethod
    def validate_description_field(cls, v: str | None) -> str | None:
        return validate_task_description(v)

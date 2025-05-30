from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from app.internal.validators import (
    TASK_DESCRIPTION_FIELD_CONFIG,
    TASK_TITLE_FIELD_CONFIG,
    validate_task_description,
    validate_task_title,
)

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .user import User


# Base class with common fields
class TaskBase(SQLModel):
    title: str = Field(index=True, **TASK_TITLE_FIELD_CONFIG)
    description: str | None = Field(default=None, **TASK_DESCRIPTION_FIELD_CONFIG)
    done: bool = Field(default=False)

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        return validate_task_title(v)

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
    title: str = Field(**TASK_TITLE_FIELD_CONFIG)
    description: str | None = Field(default=None, **TASK_DESCRIPTION_FIELD_CONFIG)

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        return validate_task_title(v)

    @field_validator("description")
    @classmethod
    def validate_description_field(cls, v: str | None) -> str | None:
        return validate_task_description(v)


# Update schema (for updating existing tasks)
class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, **TASK_TITLE_FIELD_CONFIG)
    description: str | None = Field(default=None, **TASK_DESCRIPTION_FIELD_CONFIG)
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title_field(cls, v: str | None) -> str | None:
        return validate_task_title(v)

    @field_validator("description")
    @classmethod
    def validate_description_field(cls, v: str | None) -> str | None:
        return validate_task_description(v)

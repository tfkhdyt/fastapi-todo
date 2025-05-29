from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .user import User


# Base class with common fields
class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    done: bool = Field(default=False)


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
    title: str
    description: str | None = None


# Update schema (for updating existing tasks)
class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

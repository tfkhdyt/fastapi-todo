from sqlmodel import Field, SQLModel


# Base class with common fields
class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    done: bool = Field(default=False)


# Table model
class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)


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

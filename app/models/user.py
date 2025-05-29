from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .task import Task


# Base class with common fields
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)


# Public class for returning user data (excludes sensitive fields)
class UserPublic(UserBase):
    id: int


# Create class for user registration (includes password, not hashed_password)
class UserCreate(UserBase):
    password: str


# Update class for user updates (all fields optional)
class UserUpdate(SQLModel):
    username: str | None = None
    password: str | None = None


# Database table model
class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    password: str
    # Use string forward reference
    tasks: list["Task"] = Relationship(back_populates="user")

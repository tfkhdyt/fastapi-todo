from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from app.internal.core.validators import (
    PASSWORD_FIELD_CONFIG,
    USERNAME_FIELD_CONFIG,
    validate_password,
    validate_username,
)

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .task import Task


# Base class with common fields
class UserBase(SQLModel):
    username: str = Field(
        unique=True,
        min_length=3,
        max_length=50,
        description="Username must be 3-50 characters long",
    )

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, v: str) -> str:
        validated = validate_username(v)
        if validated is None:
            raise ValueError("Username cannot be None")
        return validated


# Public class for returning user data (excludes sensitive fields)
class UserPublic(UserBase):
    id: int


# Create class for user registration (includes password, not hashed_password)
class UserCreate(UserBase):
    password: str = Field(**PASSWORD_FIELD_CONFIG)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str) -> str:
        validated = validate_password(v)
        if validated is None:
            raise ValueError("Password cannot be None")
        return validated


# Update class for user updates (all fields optional)
class UserUpdate(SQLModel):
    username: str | None = Field(default=None, **USERNAME_FIELD_CONFIG)
    password: str | None = Field(default=None, **PASSWORD_FIELD_CONFIG)

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, v: str | None) -> str | None:
        return validate_username(v)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str | None) -> str | None:
        return validate_password(v)


# Database table model
class User(UserBase, table=True):
    __tablename__: str = "users"

    id: int | None = Field(default=None, primary_key=True)
    password: str  # This stores the hashed password
    # Use string forward reference
    tasks: list["Task"] = Relationship(back_populates="user")

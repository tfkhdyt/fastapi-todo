from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .task_tag_link import TaskTagLink

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from .task import Task


class TagBase(SQLModel):
    name: str = Field(min_length=3, max_length=50)


class Tag(TagBase, table=True):
    __tablename__: str = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=50)
    user_id: int = Field(foreign_key="users.id")
    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)


class TagPublic(TagBase):
    id: int


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass

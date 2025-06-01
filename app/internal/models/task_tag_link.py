from sqlmodel import Field, SQLModel


class TaskTagLink(SQLModel, table=True):
    __tablename__ = "task_tag_links"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

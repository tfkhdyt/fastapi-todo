from sqlmodel import Field, SQLModel


class TagBase(SQLModel):
    name: str = Field(min_length=3, max_length=50)


class Tag(TagBase, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=50)
    user_id: int = Field(foreign_key="users.id")


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass

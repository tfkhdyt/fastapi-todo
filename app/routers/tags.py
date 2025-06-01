from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import desc, select

from app.internal.core.db import SessionDep
from app.internal.core.security import CurrentUserDep
from app.internal.models import Tag
from app.internal.models.tag import TagCreate, TagPublic, TagUpdate

router = APIRouter(tags=["tags"])


@router.get("/tags", response_model=list[TagPublic])
async def get_all_tags(current_user: CurrentUserDep, session: SessionDep):
    result = await session.exec(
        select(Tag).where(Tag.user_id == current_user.id).order_by(desc(Tag.id))
    )
    tags = result.all()
    return tags


@router.post("/tags", response_model=TagPublic, status_code=201)
async def create_tag(
    payload: TagCreate, current_user: CurrentUserDep, session: SessionDep
):
    tag_db = Tag(name=payload.name, user_id=current_user.id)

    session.add(tag_db)
    await session.commit()
    await session.refresh(tag_db)

    return tag_db


async def get_my_tag(tag_id: int, current_user: CurrentUserDep, session: SessionDep):
    result = await session.get(Tag, tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")

    if result.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this tag")

    return result


GetMyTagDep = Annotated[Tag, Depends(get_my_tag)]


@router.get("/tags/{tag_id}", response_model=TagPublic)
async def get_tag_by_id(tag: GetMyTagDep):
    return tag


@router.patch("/tags/{tag_id}", response_model=TagPublic)
async def update_tag(tag: GetMyTagDep, payload: TagUpdate, session: SessionDep):
    tag.sqlmodel_update(payload.model_dump(exclude_unset=True))

    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return tag


@router.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(tag: GetMyTagDep, session: SessionDep):
    await session.delete(tag)
    await session.commit()

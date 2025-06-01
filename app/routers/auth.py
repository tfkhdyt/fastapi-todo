import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.internal.core.db import SessionDep
from app.internal.core.security import (
    CurrentUserDep,
    SettingsDep,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.internal.models.jwt import Token, TokenData
from app.internal.models.user import User, UserCreate, UserPublic

router = APIRouter(tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/auth/sign-up", response_model=UserPublic, status_code=201)
async def signUp(payload: UserCreate, session: SessionDep):
    existing_user_result = await session.exec(
        select(User).where(User.username == payload.username)
    )
    existing_user = existing_user_result.first()
    if existing_user:
        logger.warning(f"Sign-up attempt with existing username: {payload.username}")
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(payload.password)
    new_user = User(
        username=payload.username,
        password=hashed_password,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
async def signIn(
    form_data: FormDep,
    session: SessionDep,
    settings: SettingsDep,
):
    user_result = await session.exec(
        select(User).where(User.username == form_data.username)
    )
    user = user_result.first()
    if not user:
        logger.warning(f"Sign-in attempt for non-existent user: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        logger.warning(f"Invalid password attempt for user: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data=TokenData(sub=user.username),
        settings=settings,
    )
    return access_token


@router.get("/auth/me", response_model=UserPublic)
async def me(current_user: CurrentUserDep):
    return current_user

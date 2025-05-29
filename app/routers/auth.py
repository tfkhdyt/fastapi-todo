from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.internal.db import SessionDep
from app.internal.security import (
    CurrentUserDep,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.internal.settings import SettingsDep
from app.models.jwt import Token, TokenData
from app.models.user import User, UserCreate, UserPublic

router = APIRouter(tags=["auth"])


@router.post("/auth/sign-up", response_model=UserPublic, status_code=201)
def signUp(payload: UserCreate, session: SessionDep):
    existing_user = session.exec(
        select(User).where(User.username == payload.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(payload.password)
    new_user = User(
        username=payload.username,
        password=hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
def signIn(
    form_data: FormDep,
    session: SessionDep,
    settings: SettingsDep,
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Username not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(
        data=TokenData(sub=user.username),
        settings=settings,
    )

    return access_token


@router.get("/auth/me", response_model=UserPublic)
def me(current_user: CurrentUserDep):
    return current_user

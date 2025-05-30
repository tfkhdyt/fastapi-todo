from datetime import UTC, datetime, timedelta
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import select

from app.internal.db import SessionDep
from app.internal.models.jwt import Token, TokenData
from app.internal.models.user import User
from app.internal.settings import SettingsDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: TokenData,
    settings: SettingsDep,
    expires_delta: Optional[timedelta] = None,
):
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    data.exp = expire

    encoded_jwt = jwt.encode(
        data.model_dump(), settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    return Token(access_token=encoded_jwt, token_type="bearer")


def decode_token(token: str, settings: SettingsDep) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return TokenData(**payload)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Failed to decode token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    token: TokenDep,
    session: SessionDep,
    settings: SettingsDep,
):
    payload = decode_token(token, settings)
    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user_result = await session.exec(select(User).where(User.username == username))
    user = user_result.first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

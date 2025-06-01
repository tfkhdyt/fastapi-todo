from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, create_engine  # Keep for Alembic if needed
from sqlmodel.ext.asyncio.session import AsyncSession

from app.internal.core.settings import get_settings

settings = get_settings()

# Use a different URL for async, note aiosqlite driver
async_sqlite_url = f"sqlite+aiosqlite:///{settings.database.sqlite.file_name}"

# The connect_args are specific to aiosqlite and other async drivers
# For aiosqlite, check_same_thread is not needed as it's handled differently.
async_engine = create_async_engine(async_sqlite_url)

# Synchronous engine for Alembic (if it doesn't support async directly)
# or for specific synchronous tasks if any.
sync_sqlite_url = f"sqlite:///{settings.database.sqlite.file_name}"
sync_engine = create_engine(sync_sqlite_url, connect_args={"check_same_thread": False})


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


# If you need a synchronous session for Alembic's env.py or other sync parts:
def get_sync_session():
    with Session(sync_engine) as session:
        yield session

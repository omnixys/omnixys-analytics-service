"""Asynchrone Engine und Session Factory für SQLAlchemy."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from kpi.config.db import db_url, db_log_statements, db_connect_args

__all__ = ["get_async_session", "async_engine"]

# Async Engine für SQLAlchemy
async_engine = create_async_engine(
    db_url,
    echo=db_log_statements,
    connect_args=db_connect_args,
)

# Session Factory
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Erzeuge eine neue asynchrone DB-Session."""
    async with async_session_factory() as session:
        yield session

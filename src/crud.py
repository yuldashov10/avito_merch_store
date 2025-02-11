from typing import Coroutine

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from src import auth, models


async def get_user_by_username(db: AsyncSession, username: str) -> Coroutine:
    stmt: Select[tuple[models.User]] = (
        select(models.User)
        .options(selectinload(models.User.inventory))
        .where(models.User.username == username)
    )

    result: Result[tuple[models.User]] = await db.execute(stmt)

    return result.scalars().first()


async def create_user(
    db: AsyncSession, username: str, password: str
) -> Coroutine:
    hashed_password: str = auth.get_password_hash(password)
    db_user = models.User(
        username=username,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_merch_item(db: AsyncSession, name: str) -> Coroutine:
    stmt = select(models.MerchItem).where(models.MerchItem.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()

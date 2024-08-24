from collections.abc import Sequence

from core.models import Category
from core.schemas.categories import CategoryCreate, CategoryUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_categories(session: AsyncSession) -> Sequence[Category]:
    stmt = select(Category).order_by(Category.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_category(session: AsyncSession, category_create: CategoryCreate) -> Category:
    category = Category(**category_create.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def update_category(session: AsyncSession, category_id: int, category_update: CategoryUpdate) -> Category:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.scalars(stmt)
    category = result.first()

    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    for key, value in category_update.model_dump().items():
        setattr(category, key, value)

    await session.commit()
    await session.refresh(category)
    return category


async def delete_category(session: AsyncSession, category_id: int) -> None:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.scalars(stmt)
    category = result.first()

    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    await session.delete(category)
    await session.commit()

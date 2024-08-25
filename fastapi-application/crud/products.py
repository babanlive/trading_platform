from collections.abc import Sequence

from core.models import Category, Product
from core.schemas.products import ProductCreate, ProductUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_products(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_product(session: AsyncSession, product_create: ProductCreate) -> Product:
    category_id = product_create.category_id
    category_stmt = select(Category).where(Category.id == category_id)
    category_result = await session.scalars(category_stmt)
    category = category_result.first()

    if not category:
        raise HTTPException(status_code=400, detail=f'Category with id {category_id} does not exist')

    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(session: AsyncSession, product_id: int, product_update: ProductUpdate) -> Product:
    product_stmt = select(Product).where(Product.id == product_id)
    product_result = await session.scalars(product_stmt)
    product = product_result.first()

    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    category_id = product_update.category_id
    category_stmt = select(Category).where(Category.id == category_id)
    category_result = await session.scalars(category_stmt)
    category = category_result.first()

    if not category:
        raise HTTPException(status_code=400, detail=f'Category with id {category_id} does not exist')

    for key, value in product_update.model_dump().items():
        setattr(product, key, value)

    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(session: AsyncSession, product_id: int) -> None:
    product = await get_product_by_id(session=session, product_id=product_id)

    if product:
        await session.delete(product)
        await session.commit()

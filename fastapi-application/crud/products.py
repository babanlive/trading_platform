from collections.abc import Sequence

from core.models import Product
from core.schemas.products import ProductCreate, ProductUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_products(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_product(session: AsyncSession, product_create: ProductCreate) -> Product:
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(session: AsyncSession, product_id: int, product_update: ProductUpdate) -> Product:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    product = result.first()

    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
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

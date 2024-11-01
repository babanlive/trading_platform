from collections.abc import Sequence

from core.models import Category, Product
from core.schemas.products import ProductCreate, ProductUpdate
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_filtered_products(
    session: AsyncSession, name: str = None, category_id: int = None, min_price: float = None, max_price: float = None
) -> Sequence[Product]:
    filters = []
    if name:
        filters.append(Product.name.ilike(f'%{name}%'))
    if category_id:
        filters.append(Product.category_id == category_id)
    if min_price is not None:
        filters.append(Product.price >= min_price)
    if max_price is not None:
        filters.append(Product.price <= max_price)

    stmt = select(Product).where(and_(*filters)).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_product(session: AsyncSession, product_create: ProductCreate) -> Product:
    product_name = product_create.name
    category_id = product_create.category_id
    category = await session.get(Category, category_id)

    if not category:
        raise HTTPException(status_code=400, detail=f'Category with id {category_id} does not exist')

    stmt = select(Product).filter(Product.name == product_name, Product.category_id == category_id)
    result = await session.execute(stmt)
    existing_product = result.scalar()

    if existing_product:
        raise HTTPException(status_code=400, detail='Product already exists in this category')

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

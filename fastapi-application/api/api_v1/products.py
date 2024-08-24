from core.models import db_helper
from core.schemas.products import ProductCreate, ProductRead
from crud import products as crud_products
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=['Products'])


@router.get('', response_model=list[ProductRead])
async def get_products(session: AsyncSession = Depends(db_helper.session_getter)):  # noqa: B008
    return await crud_products.get_all_products(session=session)


@router.post('', response_model=ProductRead)
async def create_product(
    product_create: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    return await crud_products.create_product(session=session, product_create=product_create)


@router.put('/{product_id}', response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    return await crud_products.update_product(session=session, product_id=product_id, product_update=product_update)


@router.delete('/{product_id}')
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    await crud_products.delete_product(session=session, product_id=product_id)
    return {'message': 'Product deleted successfully'}

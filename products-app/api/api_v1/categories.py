from core.models import db_helper
from core.schemas.categories import CategoryCreate, CategoryRead
from crud import categories as crud_categories
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=['Categories'])


@router.get('', response_model=list[CategoryRead])
async def get_categories(session: AsyncSession = Depends(db_helper.session_getter)):  # noqa: B008
    return await crud_categories.get_all_categories(session=session)


@router.post('', response_model=CategoryRead)
async def create_category(
    category_create: CategoryCreate,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    return await crud_categories.create_category(session=session, category_create=category_create)


@router.put('/{category_id}', response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_update: CategoryCreate,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    return await crud_categories.update_category(
        session=session, category_id=category_id, category_update=category_update
    )


@router.delete('/{category_id}')
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    await crud_categories.delete_category(session=session, category_id=category_id)
    return {'message': 'Category deleted successfully'}

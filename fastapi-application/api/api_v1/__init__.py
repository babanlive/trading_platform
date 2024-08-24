from core.config import settings
from fastapi import APIRouter

from .categories import router as categories_router
from .products import router as products_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    router=products_router,
    prefix=settings.api.v1.products,
)

router.include_router(
    router=categories_router,
    prefix=settings.api.v1.categories,
)

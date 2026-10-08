from fastapi import APIRouter

from app.api.routes import (
    catalog,
    dishes,
    governance,
    images,
    items,
    login,
    private,
    rankings,
    reviews,
    users,
    utils,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(catalog.router)
api_router.include_router(dishes.router)
api_router.include_router(reviews.router)
api_router.include_router(governance.router)
api_router.include_router(images.router)
api_router.include_router(rankings.router)


if settings.FASTAPI_ENV == "development":
    api_router.include_router(private.router)

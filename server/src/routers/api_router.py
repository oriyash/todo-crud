from fastapi import APIRouter

from .todos_router import router as todos_router

router = APIRouter(prefix="/api")

router.include_router(todos_router)

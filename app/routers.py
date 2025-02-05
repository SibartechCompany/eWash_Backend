from fastapi import APIRouter
from app.modules.user.views_clientes import router as clientes_router

router = APIRouter()

router.include_router(clientes_router, prefix="/clientes", tags=["clientes"])




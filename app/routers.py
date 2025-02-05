from fastapi import APIRouter
from app.modules.user.views_clientes import router as clientes_router
from app.modules.vehiculo.views_vehiculo import router as vehiculos_router

router = APIRouter()

router.include_router(clientes_router, prefix="/clientes", tags=["clientes"])
router.include_router(vehiculos_router, prefix="/vehiculos", tags=["vehiculos"])



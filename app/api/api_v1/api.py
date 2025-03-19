from fastapi import APIRouter

from app.api.api_v1.endpoints import administradores, sedes, empleados, clientes, vehiculos, tipos_servicio, servicios, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(administradores.router, prefix="/administradores", tags=["administradores"])
api_router.include_router(sedes.router, prefix="/sedes", tags=["sedes"])
api_router.include_router(empleados.router, prefix="/empleados", tags=["empleados"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(vehiculos.router, prefix="/vehiculos", tags=["vehiculos"])
api_router.include_router(tipos_servicio.router, prefix="/tipos-servicio", tags=["tipos_servicio"])
api_router.include_router(servicios.router, prefix="/servicios", tags=["servicios"])
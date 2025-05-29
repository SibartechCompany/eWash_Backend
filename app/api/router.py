from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, organizations, clients, vehicles, employees, services, orders, dashboard, branches

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(branches.router, prefix="/branches", tags=["branches"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"]) 
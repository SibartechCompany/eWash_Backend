from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.client import Client
from app.models.employee import Employee, EmployeeStatus
from app.models.service import Service
from app.models.order import Order, OrderStatus
from app.models.vehicle import Vehicle

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtener estadísticas del dashboard para la organización del usuario
    """
    org_id = current_user.organization_id
    
    # Fecha actual y hace 30 días
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    # Contar clientes totales
    clients_result = await db.execute(
        select(func.count(Client.id)).where(
            and_(Client.organization_id == org_id, Client.is_active == True)
        )
    )
    total_clients = clients_result.scalar() or 0
    
    # Contar empleados activos
    employees_result = await db.execute(
        select(func.count(Employee.id)).where(
            and_(Employee.organization_id == org_id, Employee.status == EmployeeStatus.ACTIVE)
        )
    )
    total_employees = employees_result.scalar() or 0
    
    # Contar servicios activos
    services_result = await db.execute(
        select(func.count(Service.id)).where(
            and_(Service.organization_id == org_id, Service.is_active == True)
        )
    )
    total_services = services_result.scalar() or 0
    
    # Contar órdenes del mes actual
    orders_result = await db.execute(
        select(func.count(Order.id)).where(
            and_(
                Order.organization_id == org_id,
                Order.created_at >= thirty_days_ago
            )
        )
    )
    monthly_orders = orders_result.scalar() or 0
    
    # Calcular ingresos del mes (suma de precios de órdenes completadas)
    revenue_result = await db.execute(
        select(func.sum(Order.total_amount)).where(
            and_(
                Order.organization_id == org_id,
                Order.status == OrderStatus.COMPLETED,
                Order.created_at >= thirty_days_ago
            )
        )
    )
    monthly_revenue = float(revenue_result.scalar() or 0)
    
    # Órdenes pendientes
    pending_orders_result = await db.execute(
        select(func.count(Order.id)).where(
            and_(
                Order.organization_id == org_id,
                Order.status.in_([OrderStatus.PENDING, OrderStatus.IN_PROGRESS])
            )
        )
    )
    pending_orders = pending_orders_result.scalar() or 0
    
    return {
        "total_clients": total_clients,
        "total_employees": total_employees,
        "total_services": total_services,
        "monthly_orders": monthly_orders,
        "monthly_revenue": monthly_revenue,
        "pending_orders": pending_orders,
        "organization_id": str(org_id)
    }

@router.get("/recent-orders")
async def get_recent_orders(
    limit: int = 5,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtener órdenes recientes para mostrar en el dashboard
    """
    org_id = current_user.organization_id
    
    # Obtener órdenes recientes con información del cliente, vehículo y servicio
    orders_result = await db.execute(
        select(Order, Client.full_name, Vehicle.model, Service.name)
        .join(Client, Order.client_id == Client.id)
        .join(Vehicle, Order.vehicle_id == Vehicle.id)
        .join(Service, Order.service_id == Service.id)
        .where(Order.organization_id == org_id)
        .order_by(Order.created_at.desc())
        .limit(limit)
    )
    
    orders_data = []
    for order, client_name, vehicle_model, service_name in orders_result.all():
        orders_data.append({
            "id": str(order.id),
            "order_number": order.order_number,
            "client_name": client_name,
            "vehicle_model": vehicle_model,
            "service_name": service_name,
            "status": order.status.value if hasattr(order.status, 'value') else str(order.status),
            "total_price": float(order.total_amount) if order.total_amount else 0,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "completed_at": order.completed_at.isoformat() if order.completed_at else None
        })
    
    return {
        "recent_orders": orders_data
    } 
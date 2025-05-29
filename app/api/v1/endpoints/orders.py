from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.base import CRUDBase
from app.models.order import Order
from app.models.service import Service
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.models.employee import Employee
from app.schemas.order import Order as OrderSchema, OrderCreateSimple, OrderUpdate
from app.schemas.user import User
from app.schemas.base import PaginatedResponse
from app.api.v1.dependencies import get_pagination_params
from pydantic import BaseModel

# Create CRUD instance
crud_order = CRUDBase(Order)

# Schema for optimized order response
class OrderWithRelations(BaseModel):
    id: uuid.UUID
    order_number: str
    status: str
    payment_status: str
    total_amount: str
    notes: str | None
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    
    # Related data
    client_name: str
    client_phone: str
    vehicle_brand: str  # Será el tipo de vehículo (car/motorcycle)
    vehicle_model: str
    vehicle_plate: str
    vehicle_color: str | None
    vehicle_year: int | None
    vehicle_type: str
    service_name: str
    service_price: str
    employee_name: str | None
    employee_phone: str | None
    
    class Config:
        from_attributes = True

router = APIRouter()

@router.get("/optimized", response_model=PaginatedResponse[OrderWithRelations])
async def read_orders_optimized(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve orders with all related data in a single query for optimal performance
    """
    # Query with all joins to get related data in one go
    query = (
        select(
            Order.id,
            Order.order_number,
            Order.status,
            Order.payment_status,
            Order.total_amount,
            Order.notes,
            Order.scheduled_at,
            Order.completed_at,
            Order.created_at,
            Order.updated_at,
            Client.full_name.label('client_name'),
            Client.phone.label('client_phone'),
            Vehicle.model.label('vehicle_model'),
            Vehicle.plate.label('vehicle_plate'),
            Vehicle.color.label('vehicle_color'),
            Vehicle.year.label('vehicle_year'),
            Vehicle.vehicle_type.label('vehicle_type'),
            Service.name.label('service_name'),
            Service.price.label('service_price'),
            Employee.full_name.label('employee_name'),
            Employee.phone.label('employee_phone')
        )
        .join(Vehicle, Order.vehicle_id == Vehicle.id)
        .join(Client, Vehicle.client_id == Client.id)
        .join(Service, Order.service_id == Service.id)
        .outerjoin(Employee, Order.assigned_employee_id == Employee.id)
        .where(
            and_(
                Order.organization_id == current_user.organization_id,
                Order.is_active == True
            )
        )
        .order_by(Order.created_at.desc())
    )
    
    # Count total with same filters
    count_query = (
        select(func.count())
        .select_from(Order)
        .join(Vehicle, Order.vehicle_id == Vehicle.id)
        .join(Client, Vehicle.client_id == Client.id)
        .join(Service, Order.service_id == Service.id)
        .outerjoin(Employee, Order.assigned_employee_id == Employee.id)
        .where(
            and_(
                Order.organization_id == current_user.organization_id,
                Order.is_active == True
            )
        )
    )
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    rows = result.all()
    
    # Transform to OrderWithRelations objects
    orders = []
    for row in rows:
        order_data = {
            'id': row.id,
            'order_number': row.order_number,
            'status': row.status,
            'payment_status': row.payment_status,
            'total_amount': str(row.total_amount),
            'notes': row.notes,
            'scheduled_at': row.scheduled_at,
            'completed_at': row.completed_at,
            'created_at': row.created_at,
            'updated_at': row.updated_at,
            'client_name': row.client_name,
            'client_phone': row.client_phone,
            'vehicle_brand': row.vehicle_type.title(),  # Usamos el tipo como marca
            'vehicle_model': row.vehicle_model,
            'vehicle_plate': row.vehicle_plate,
            'vehicle_color': row.vehicle_color,
            'vehicle_year': row.vehicle_year,
            'vehicle_type': row.vehicle_type,
            'service_name': row.service_name,
            'service_price': str(row.service_price),
            'employee_name': row.employee_name or "Sin asignar",
            'employee_phone': row.employee_phone or ""
        }
        orders.append(OrderWithRelations(**order_data))
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=orders,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.get("/", response_model=PaginatedResponse[OrderSchema])
async def read_orders(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve orders from current organization with pagination
    """
    # Base query
    query = select(Order).where(
        and_(
            Order.organization_id == current_user.organization_id,
            Order.is_active == True
        )
    )
    
    # Count total
    count_query = select(func.count(Order.id)).where(
        and_(
            Order.organization_id == current_user.organization_id,
            Order.is_active == True
        )
    )
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=orders,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.post("/", response_model=OrderSchema)
async def create_order(
    *,
    db: AsyncSession = Depends(get_db),
    order_in: OrderCreateSimple,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new order
    """
    # Verificar que el servicio existe y pertenece a la organización
    service_query = select(Service).where(Service.id == order_in.service_id)
    service_result = await db.execute(service_query)
    service = service_result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Service does not belong to your organization")
    
    # Verificar que el vehículo existe y su cliente pertenece a la organización
    vehicle_query = select(Vehicle).join(Client).where(Vehicle.id == order_in.vehicle_id)
    vehicle_result = await db.execute(vehicle_query)
    vehicle = vehicle_result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Verificar que el cliente del vehículo pertenece a la organización
    client_query = select(Client).where(Client.id == vehicle.client_id)
    client_result = await db.execute(client_query)
    client = client_result.scalar_one_or_none()
    
    if not client or client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Vehicle does not belong to a client in your organization")
    
    # Generar número de orden único
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    
    # Crear la orden
    order_data = {
        "order_number": order_number,
        "client_id": client.id,
        "vehicle_id": order_in.vehicle_id,
        "service_id": order_in.service_id,
        "assigned_employee_id": order_in.assigned_employee_id,
        "total_amount": service.price,
        "notes": order_in.notes,
        "scheduled_at": order_in.scheduled_at,
        "organization_id": current_user.organization_id,
        "status": "pending",
        "payment_status": "pending"
    }
    
    order = await crud_order.create(db, obj_in=order_data)
    return order

@router.get("/{order_id}", response_model=OrderSchema)
async def read_order(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get order by id.
    """
    order = await crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

@router.put("/{order_id}", response_model=OrderSchema)
async def update_order(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: uuid.UUID,
    order_in: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an order.
    """
    order = await crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    order = await crud_order.update(db=db, db_obj=order, obj_in=order_in)
    return order

@router.delete("/{order_id}", response_model=OrderSchema)
async def delete_order(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an order (soft delete by setting is_active to False).
    """
    order = await crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Soft delete
    order = await crud_order.update(db=db, db_obj=order, obj_in={"is_active": False})
    return order

@router.patch("/{order_id}/status")
async def update_order_status(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: uuid.UUID,
    status: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update only the status of an order.
    """
    order = await crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Validate status
    valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    # Update completed_at if status is completed
    update_data = {"status": status}
    if status == "completed":
        update_data["completed_at"] = datetime.utcnow()
    elif status == "pending":
        update_data["completed_at"] = None
    
    order = await crud_order.update(db=db, db_obj=order, obj_in=update_data)
    return {"message": "Status updated successfully", "status": order.status} 
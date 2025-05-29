from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, or_
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.base import CRUDBase
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.schemas.vehicle import Vehicle as VehicleSchema, VehicleCreate, VehicleUpdate
from app.schemas.user import User
from app.api.v1.dependencies import get_pagination_params

# Create CRUD instance
crud_vehicle = CRUDBase(Vehicle)

router = APIRouter()

@router.get("/", response_model=List[VehicleSchema])
async def read_vehicles(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
    client_id: Optional[str] = Query(None, description="Filter vehicles by client ID"),
) -> Any:
    """
    Retrieve vehicles from current organization
    """
    # Base query for vehicles that belong to clients of the current organization
    query = select(Vehicle).join(Client).where(
        and_(
            Client.organization_id == current_user.organization_id,
            Vehicle.is_active == True
        )
    )
    
    # Add client_id filter if provided
    if client_id:
        try:
            client_uuid = uuid.UUID(client_id)
            query = query.where(Vehicle.client_id == client_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid client_id format")
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    result = await db.execute(query)
    vehicles = result.scalars().all()
    return vehicles

@router.post("/", response_model=VehicleSchema)
async def create_vehicle(
    *,
    db: AsyncSession = Depends(get_db),
    vehicle_in: VehicleCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new vehicle
    """
    # Verify that the client belongs to the current organization
    client_query = select(Client).where(Client.id == vehicle_in.client_id)
    client_result = await db.execute(client_query)
    client = client_result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    vehicle = await crud_vehicle.create(db, obj_in=vehicle_in)
    return vehicle

@router.get("/search", response_model=VehicleSchema)
async def search_vehicle_by_plate(
    plate: str = Query(..., description="Vehicle plate to search for"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Search vehicle by plate number (exact match)
    """
    # Query vehicle with client information
    query = select(Vehicle).options(selectinload(Vehicle.client)).join(Client).where(
        and_(
            Vehicle.plate.ilike(f"%{plate}%"),
            Client.organization_id == current_user.organization_id,
            Vehicle.is_active == True
        )
    )
    
    result = await db.execute(query)
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return vehicle

@router.get("/autocomplete", response_model=List[VehicleSchema])
async def autocomplete_vehicles(
    q: str = Query(..., min_length=1, description="Search query for vehicle plate or model"),
    limit: int = Query(10, le=20, description="Maximum number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Autocomplete vehicles by plate or model
    """
    # Query vehicles with client information
    query = select(Vehicle).options(selectinload(Vehicle.client)).join(Client).where(
        and_(
            or_(
                Vehicle.plate.ilike(f"%{q}%"),
                Vehicle.model.ilike(f"%{q}%")
            ),
            Client.organization_id == current_user.organization_id,
            Vehicle.is_active == True
        )
    ).limit(limit)
    
    result = await db.execute(query)
    vehicles = result.scalars().all()
    
    return vehicles

@router.get("/{vehicle_id}", response_model=VehicleSchema)
async def read_vehicle(
    *,
    db: AsyncSession = Depends(get_db),
    vehicle_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get vehicle by ID
    """
    # Query vehicle with client information
    query = select(Vehicle).options(selectinload(Vehicle.client)).where(
        Vehicle.id == vehicle_id
    )
    result = await db.execute(query)
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Check if vehicle belongs to current organization through client
    if vehicle.client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleSchema)
async def update_vehicle(
    *,
    db: AsyncSession = Depends(get_db),
    vehicle_id: uuid.UUID,
    vehicle_in: VehicleUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update vehicle
    """
    # Get vehicle with client
    query = select(Vehicle).options(selectinload(Vehicle.client)).where(
        Vehicle.id == vehicle_id
    )
    result = await db.execute(query)
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Check permissions
    if vehicle.client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    vehicle = await crud_vehicle.update(db, db_obj=vehicle, obj_in=vehicle_in)
    return vehicle

@router.delete("/{vehicle_id}", response_model=VehicleSchema)
async def delete_vehicle(
    *,
    db: AsyncSession = Depends(get_db),
    vehicle_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete vehicle (soft delete)
    """
    # Get vehicle with client
    query = select(Vehicle).options(selectinload(Vehicle.client)).where(
        Vehicle.id == vehicle_id
    )
    result = await db.execute(query)
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Check permissions
    if vehicle.client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    vehicle = await crud_vehicle.remove(db, id=vehicle_id)
    return vehicle 
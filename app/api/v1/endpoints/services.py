from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.base import CRUDBase
from app.models.service import Service
from app.schemas.service import Service as ServiceSchema, ServiceCreate, ServiceUpdate
from app.schemas.user import User
from app.schemas.base import PaginatedResponse
from app.api.v1.dependencies import get_pagination_params

# Create CRUD instance
crud_service = CRUDBase(Service)

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[ServiceSchema])
async def read_services(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search by name or description"),
    vehicle_type: Optional[str] = Query(None, description="Filter by vehicle type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve services from current organization with pagination
    """
    # Base query
    query = select(Service).where(
        and_(
            Service.organization_id == current_user.organization_id,
            Service.is_active == True
        )
    )
    
    # Add search filter if provided
    if search:
        search_filter = or_(
            Service.name.ilike(f"%{search}%"),
            Service.description.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Add vehicle type filter if provided
    if vehicle_type and vehicle_type in ["car", "motorcycle"]:
        query = query.where(Service.vehicle_type == vehicle_type)
    
    # Add active status filter if provided
    if is_active is not None:
        query = query.where(Service.is_active == is_active)
    
    # Count total
    count_query = select(func.count(Service.id)).where(
        and_(
            Service.organization_id == current_user.organization_id,
            Service.is_active == True
        )
    )
    
    # Add filters to count query
    if search:
        search_filter = or_(
            Service.name.ilike(f"%{search}%"),
            Service.description.ilike(f"%{search}%")
        )
        count_query = count_query.where(search_filter)
    
    if vehicle_type and vehicle_type in ["car", "motorcycle"]:
        count_query = count_query.where(Service.vehicle_type == vehicle_type)
    
    if is_active is not None:
        count_query = count_query.where(Service.is_active == is_active)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    services = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=services,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.post("/", response_model=ServiceSchema)
async def create_service(
    *,
    db: AsyncSession = Depends(get_db),
    service_in: ServiceCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new service
    """
    # Check if service with same name already exists
    existing_query = select(Service).where(
        and_(
            Service.name == service_in.name,
            Service.organization_id == current_user.organization_id
        )
    )
    existing_result = await db.execute(existing_query)
    existing_service = existing_result.scalar_one_or_none()
    
    if existing_service:
        raise HTTPException(
            status_code=400,
            detail="Service with this name already exists"
        )
    
    # Create service
    service_data = {
        **service_in.model_dump(),
        "organization_id": current_user.organization_id
    }
    
    service = await crud_service.create(db, obj_in=service_data)
    return service

@router.get("/{service_id}", response_model=ServiceSchema)
async def read_service(
    *,
    db: AsyncSession = Depends(get_db),
    service_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get service by ID
    """
    service = await crud_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if service belongs to current organization
    if service.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return service

@router.put("/{service_id}", response_model=ServiceSchema)
async def update_service(
    *,
    db: AsyncSession = Depends(get_db),
    service_id: uuid.UUID,
    service_in: ServiceUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update service
    """
    service = await crud_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if service belongs to current organization
    if service.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    service = await crud_service.update(db, db_obj=service, obj_in=service_in)
    return service

@router.delete("/{service_id}", response_model=ServiceSchema)
async def delete_service(
    *,
    db: AsyncSession = Depends(get_db),
    service_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete service (soft delete)
    """
    service = await crud_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if service belongs to current organization
    if service.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    service = await crud_service.remove(db, id=service_id)
    return service

@router.patch("/{service_id}/toggle-status", response_model=ServiceSchema)
async def toggle_service_status(
    *,
    db: AsyncSession = Depends(get_db),
    service_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Toggle service status (active/inactive)
    """
    service = await crud_service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if service belongs to current organization
    if service.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Toggle status
    new_status = not service.is_active
    
    service = await crud_service.update(
        db, 
        db_obj=service, 
        obj_in={"is_active": new_status}
    )
    return service 
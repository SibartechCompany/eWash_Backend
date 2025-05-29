from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func, and_, or_
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.client import client as crud_client
from app.schemas.client import ClientWithVehicles, ClientCreate, ClientUpdate
from app.schemas.user import User
from app.schemas.base import PaginatedResponse
from app.api.v1.dependencies import get_pagination_params
from app.models.client import Client as ClientModel

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[ClientWithVehicles])
async def read_clients(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search by name, phone, or email"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve clients from current organization with pagination
    """
    # Base query with vehicles loaded
    query = select(ClientModel).options(selectinload(ClientModel.vehicles)).where(
        and_(
            ClientModel.organization_id == current_user.organization_id,
            ClientModel.is_active == True
        )
    )
    
    # Add search filter if provided
    if search:
        search_filter = or_(
            ClientModel.full_name.ilike(f"%{search}%"),
            ClientModel.phone.ilike(f"%{search}%"),
            ClientModel.email.ilike(f"%{search}%") if search else False
        )
        query = query.where(search_filter)
    
    # Count total (without vehicles to avoid complex joins)
    count_query = select(func.count(ClientModel.id)).where(
        and_(
            ClientModel.organization_id == current_user.organization_id,
            ClientModel.is_active == True
        )
    )
    
    # Add search filter to count query if provided
    if search:
        search_filter = or_(
            ClientModel.full_name.ilike(f"%{search}%"),
            ClientModel.phone.ilike(f"%{search}%"),
            ClientModel.email.ilike(f"%{search}%") if search else False
        )
        count_query = count_query.where(search_filter)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    clients = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=clients,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.get("/search", response_model=List[ClientWithVehicles])
async def search_clients(
    *,
    db: AsyncSession = Depends(get_db),
    q: str = Query(..., min_length=2, description="Search query"),
    pagination: dict = Depends(get_pagination_params),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Search clients by name, phone, or email
    """
    # Query with vehicles loaded
    query = select(ClientModel).options(selectinload(ClientModel.vehicles)).where(
        and_(
            or_(
                ClientModel.full_name.ilike(f"%{q}%"),
                ClientModel.phone.ilike(f"%{q}%"),
                ClientModel.email.ilike(f"%{q}%") if q else False
            ),
            ClientModel.organization_id == current_user.organization_id,
            ClientModel.is_active == True
        )
    ).offset(pagination["skip"]).limit(pagination["limit"])
    
    result = await db.execute(query)
    clients = result.scalars().all()
    return clients

@router.post("/", response_model=ClientWithVehicles)
async def create_client(
    *,
    db: AsyncSession = Depends(get_db),
    client_in: ClientCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new client
    """
    # Ensure client is created in current organization
    client_data = client_in.dict()
    client_data["organization_id"] = current_user.organization_id
    
    # Check if client with same phone already exists
    existing_client = await crud_client.get_by_phone(
        db, phone=client_in.phone, organization_id=current_user.organization_id
    )
    if existing_client:
        raise HTTPException(
            status_code=400,
            detail="Client with this phone number already exists"
        )
    
    client = await crud_client.create(db, obj_in=client_data)
    return client

@router.get("/{client_id}", response_model=ClientWithVehicles)
async def read_client(
    *,
    db: AsyncSession = Depends(get_db),
    client_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get client by ID
    """
    # Query with vehicles included
    query = select(ClientModel).options(selectinload(ClientModel.vehicles)).where(
        ClientModel.id == client_id
    )
    result = await db.execute(query)
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client belongs to current organization
    if client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return client

@router.put("/{client_id}", response_model=ClientWithVehicles)
async def update_client(
    *,
    db: AsyncSession = Depends(get_db),
    client_id: uuid.UUID,
    client_in: ClientUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update client
    """
    # Query with vehicles included
    query = select(ClientModel).options(selectinload(ClientModel.vehicles)).where(
        ClientModel.id == client_id
    )
    result = await db.execute(query)
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client belongs to current organization
    if client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    client = await crud_client.update(db, db_obj=client, obj_in=client_in)
    return client

@router.delete("/{client_id}", response_model=ClientWithVehicles)
async def delete_client(
    *,
    db: AsyncSession = Depends(get_db),
    client_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete client (soft delete)
    """
    # Query with vehicles included
    query = select(ClientModel).options(selectinload(ClientModel.vehicles)).where(
        ClientModel.id == client_id
    )
    result = await db.execute(query)
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client belongs to current organization
    if client.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    client = await crud_client.remove(db, id=client_id)
    return client 
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.crud.organization import organization as crud_organization
from app.schemas.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Organization])
async def read_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Retrieve organizations (superuser only)
    """
    organizations = await crud_organization.get_multi(db)
    return organizations

@router.get("/me", response_model=Organization)
async def read_my_organization(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's organization
    """
    organization = await crud_organization.get(db, id=current_user.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put("/me", response_model=Organization)
async def update_my_organization(
    *,
    db: AsyncSession = Depends(get_db),
    organization_in: OrganizationUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user's organization
    """
    organization = await crud_organization.get(db, id=current_user.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    organization = await crud_organization.update(db, db_obj=organization, obj_in=organization_in)
    return organization 
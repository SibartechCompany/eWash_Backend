from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.organization import Organization
import uuid

async def get_current_user_organization(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Organization:
    """Get current user's organization"""
    if not current_user.organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return current_user.organization

async def verify_organization_access(
    organization_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user)
) -> bool:
    """Verify if user has access to organization"""
    if current_user.is_superuser:
        return True
    
    if current_user.organization_id == organization_id:
        return True
    
    # Check if it's a parent organization (for main admins)
    # This would need additional logic based on your hierarchy needs
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions to access this organization"
    )

def get_pagination_params(skip: int = 0, limit: int = 100):
    """Get pagination parameters"""
    if limit > 100:
        limit = 100
    return {"skip": skip, "limit": limit} 
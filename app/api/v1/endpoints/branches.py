from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.branch import branch as crud_branch
from app.schemas.branch import Branch, BranchCreate, BranchUpdate
from app.schemas.user import User
from app.schemas.base import PaginatedResponse
from app.api.v1.dependencies import get_pagination_params
from app.models.branch import Branch as BranchModel

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[Branch])
async def read_branches(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search by name, code, or address"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve branches from current organization with pagination
    """
    # Base query
    query = select(BranchModel).where(
        and_(
            BranchModel.organization_id == current_user.organization_id,
            BranchModel.is_active == True
        )
    )
    
    # Add search filter if provided
    if search:
        search_filter = or_(
            BranchModel.name.ilike(f"%{search}%"),
            BranchModel.code.ilike(f"%{search}%"),
            BranchModel.address.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Count total
    count_query = select(func.count(BranchModel.id)).where(
        and_(
            BranchModel.organization_id == current_user.organization_id,
            BranchModel.is_active == True
        )
    )
    
    # Add search filter to count query if provided
    if search:
        search_filter = or_(
            BranchModel.name.ilike(f"%{search}%"),
            BranchModel.code.ilike(f"%{search}%"),
            BranchModel.address.ilike(f"%{search}%")
        )
        count_query = count_query.where(search_filter)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    branches = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=branches,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.post("/", response_model=Branch)
async def create_branch(
    *,
    db: AsyncSession = Depends(get_db),
    branch_in: BranchCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new branch
    """
    # Check if branch with same code already exists
    existing_branch = await crud_branch.get_by_code(
        db, code=branch_in.code, organization_id=current_user.organization_id
    )
    if existing_branch:
        raise HTTPException(
            status_code=400,
            detail="Branch with this code already exists"
        )
    
    # Ensure branch is created in current organization
    branch_data = branch_in.dict()
    branch_data["organization_id"] = current_user.organization_id
    
    branch = await crud_branch.create(db, obj_in=branch_data)
    return branch

@router.get("/{branch_id}", response_model=Branch)
async def read_branch(
    *,
    db: AsyncSession = Depends(get_db),
    branch_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get branch by ID
    """
    branch = await crud_branch.get(db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Check if branch belongs to current organization
    if branch.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return branch

@router.put("/{branch_id}", response_model=Branch)
async def update_branch(
    *,
    db: AsyncSession = Depends(get_db),
    branch_id: uuid.UUID,
    branch_in: BranchUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update branch
    """
    branch = await crud_branch.get(db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Check if branch belongs to current organization
    if branch.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    branch = await crud_branch.update(db, db_obj=branch, obj_in=branch_in)
    return branch

@router.delete("/{branch_id}", response_model=Branch)
async def delete_branch(
    *,
    db: AsyncSession = Depends(get_db),
    branch_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete branch (soft delete)
    """
    branch = await crud_branch.get(db, id=branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Check if branch belongs to current organization
    if branch.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    branch = await crud_branch.remove(db, id=branch_id)
    return branch 
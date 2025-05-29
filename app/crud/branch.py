from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
import uuid

from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate

class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    async def get_by_code(
        self, db: AsyncSession, *, code: str, organization_id: uuid.UUID
    ) -> Optional[Branch]:
        """Get branch by code within organization"""
        query = select(Branch).where(
            and_(
                Branch.code == code,
                Branch.organization_id == organization_id,
                Branch.is_active == True
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_organization(
        self, db: AsyncSession, *, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Branch]:
        """Get all branches for an organization"""
        query = select(Branch).where(
            and_(
                Branch.organization_id == organization_id,
                Branch.is_active == True
            )
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def search_branches(
        self, 
        db: AsyncSession, 
        *, 
        query: str, 
        organization_id: uuid.UUID,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Branch]:
        """Search branches by name, code, or address"""
        search_query = select(Branch).where(
            and_(
                Branch.organization_id == organization_id,
                Branch.is_active == True,
                or_(
                    Branch.name.ilike(f"%{query}%"),
                    Branch.code.ilike(f"%{query}%"),
                    Branch.address.ilike(f"%{query}%")
                )
            )
        ).offset(skip).limit(limit)
        result = await db.execute(search_query)
        return result.scalars().all()

branch = CRUDBranch(Branch) 
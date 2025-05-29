from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
import uuid

class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Organization]:
        """Get organization by email"""
        result = await db.execute(select(Organization).where(Organization.email == email))
        return result.scalar_one_or_none()

    async def get_by_tax_id(self, db: AsyncSession, *, tax_id: str) -> Optional[Organization]:
        """Get organization by tax ID"""
        result = await db.execute(select(Organization).where(Organization.tax_id == tax_id))
        return result.scalar_one_or_none()

    async def get_sub_organizations(self, db: AsyncSession, *, parent_id: uuid.UUID) -> List[Organization]:
        """Get sub-organizations of a parent organization"""
        result = await db.execute(
            select(Organization).where(Organization.parent_organization_id == parent_id)
        )
        return result.scalars().all()

# Create instance
organization = CRUDOrganization(Organization) 
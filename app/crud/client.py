from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
import uuid

class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    async def get_by_phone(self, db: AsyncSession, *, phone: str, organization_id: uuid.UUID) -> Optional[Client]:
        """Get client by phone number within organization"""
        result = await db.execute(
            select(Client).where(
                Client.phone == phone,
                Client.organization_id == organization_id
            )
        )
        return result.scalar_one_or_none()

    async def search_clients(
        self, 
        db: AsyncSession, 
        *, 
        query: str, 
        organization_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Client]:
        """Search clients by name, phone, or email"""
        search_query = select(Client).where(
            Client.organization_id == organization_id,
            Client.is_active == True,
            or_(
                Client.full_name.ilike(f"%{query}%"),
                Client.phone.ilike(f"%{query}%"),
                Client.email.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit)
        
        result = await db.execute(search_query)
        return result.scalars().all()

# Create instance
client = CRUDClient(Client) 
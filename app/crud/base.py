from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.core.database import Base
import uuid

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    async def get(self, db: AsyncSession, id: uuid.UUID) -> Optional[ModelType]:
        """Get a single record by ID"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        organization_id: Optional[uuid.UUID] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        query = select(self.model)
        
        # Filter by organization if the model has organization_id
        if organization_id and hasattr(self.model, 'organization_id'):
            query = query.where(self.model.organization_id == organization_id)
        
        # Filter only active records
        if hasattr(self.model, 'is_active'):
            query = query.where(self.model.is_active == True)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record"""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: uuid.UUID) -> Optional[ModelType]:
        """Soft delete a record (set is_active to False)"""
        db_obj = await self.get(db, id=id)
        if db_obj:
            if hasattr(db_obj, 'is_active'):
                db_obj.is_active = False
                db.add(db_obj)
                await db.commit()
                await db.refresh(db_obj)
            else:
                await db.delete(db_obj)
                await db.commit()
        return db_obj

    async def hard_delete(self, db: AsyncSession, *, id: uuid.UUID) -> Optional[ModelType]:
        """Hard delete a record from database"""
        db_obj = await self.get(db, id=id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

    async def count(
        self, 
        db: AsyncSession, 
        organization_id: Optional[uuid.UUID] = None
    ) -> int:
        """Count records"""
        query = select(self.model)
        
        if organization_id and hasattr(self.model, 'organization_id'):
            query = query.where(self.model.organization_id == organization_id)
        
        if hasattr(self.model, 'is_active'):
            query = query.where(self.model.is_active == True)
            
        result = await db.execute(query)
        return len(result.scalars().all()) 
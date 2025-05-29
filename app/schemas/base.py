from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, TypeVar, Generic
import uuid

T = TypeVar('T')

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseInDB(BaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

class BaseCreate(BaseModel):
    pass

class BaseUpdate(BaseModel):
    pass

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True) 
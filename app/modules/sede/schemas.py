from typing import Optional, List
from pydantic import BaseModel, validator
import re

# Shared properties
class SedeBase(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    ciudad: str
    activa: bool = True
    
    @validator('telefono')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

# Properties to receive on item creation
class SedeCreate(SedeBase):
    id_admin: int

# Properties to receive on item update
class SedeUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    activa: Optional[bool] = None
    id_admin: Optional[int] = None
    
    @validator('telefono')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

# Properties shared by models stored in DB
class SedeInDBBase(SedeBase):
    id_sede: int
    id_admin: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Sede(SedeInDBBase):
    pass

# Properties stored in DB
class SedeInDB(SedeInDBBase):
    pass

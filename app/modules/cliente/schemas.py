from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
import re

# Shared properties
class ClienteBase(BaseModel):
    nombre_completo: str
    telefono: str
    email: EmailStr
    direccion: str
    
    @validator('telefono')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

# Properties to receive on item creation
class ClienteCreate(ClienteBase):
    pass

# Properties to receive on item update
class ClienteUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    
    @validator('telefono')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

# Properties shared by models stored in DB
class ClienteInDBBase(ClienteBase):
    id_cliente: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Cliente(ClienteInDBBase):
    pass

# Properties stored in DB
class ClienteInDB(ClienteInDBBase):
    pass

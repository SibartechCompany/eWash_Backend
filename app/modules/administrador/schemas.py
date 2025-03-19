from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
import re

# Shared properties
class AdministradorBase(BaseModel):
    nombre_completo: str
    usuario: str
    email: EmailStr
    telefono: str
    
    @validator('telefono')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

# Properties to receive on item creation
class AdministradorCreate(AdministradorBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v

# Properties to receive on item update
class AdministradorUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v

# Properties shared by models stored in DB
class AdministradorInDBBase(AdministradorBase):
    id_admin: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Administrador(AdministradorInDBBase):
    pass

# Properties stored in DB
class AdministradorInDB(AdministradorInDBBase):
    password: str

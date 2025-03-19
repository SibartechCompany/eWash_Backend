from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import date
import re

# Shared properties
class EmpleadoBase(BaseModel):
    nombre_completo: str
    tipo_documento: str
    numero_documento: str
    cargo: str
    telefono: str
    email: EmailStr
    direccion: str
    fecha_inicio: date = date.today()
    estado: str = "activo"
    
    @validator('telefono')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v
    
    @validator('estado')
    def validate_estado(cls, v):
        valid_states = ["activo", "inactivo", "suspendido", "vacaciones"]
        if v.lower() not in valid_states:
            raise ValueError(f'Estado must be one of: {", ".join(valid_states)}')
        return v.lower()

# Properties to receive on item creation
class EmpleadoCreate(EmpleadoBase):
    id_sede: int

# Properties to receive on item update
class EmpleadoUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    cargo: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    estado: Optional[str] = None
    id_sede: Optional[int] = None
    
    @validator('telefono')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\+?[0-9]{8,15}$', v):
            raise ValueError('Invalid phone number format')
        return v
    
    @validator('estado')
    def validate_estado(cls, v):
        if v is None:
            return v
        valid_states = ["activo", "inactivo", "suspendido", "vacaciones"]
        if v.lower() not in valid_states:
            raise ValueError(f'Estado must be one of: {", ".join(valid_states)}')
        return v.lower()

# Properties shared by models stored in DB
class EmpleadoInDBBase(EmpleadoBase):
    id_empleado: int
    id_sede: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Empleado(EmpleadoInDBBase):
    pass

# Properties stored in DB
class EmpleadoInDB(EmpleadoInDBBase):
    pass

from typing import Optional, List
from pydantic import BaseModel, validator
import re
from datetime import datetime

# Shared properties
class VehiculoBase(BaseModel):
    placa: str
    tipo: str
    marca: str
    modelo: str
    año: int  # Añadido el campo año
    color: str
    
    @validator('tipo')
    def validate_tipo(cls, v):
        valid_types = ["carro", "moto"]
        if v.lower() not in valid_types:
            raise ValueError(f'Tipo must be one of: {", ".join(valid_types)}')
        return v.lower()
    
    @validator('placa')
    def validate_placa(cls, v):
        # Simple validation for Colombian license plates
        if not re.match(r'^[A-Z0-9]{5,7}$', v.upper()):
            raise ValueError('Invalid license plate format')
        return v.upper()
    
    @validator('año')
    def validate_año(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

# Properties to receive on item creation
class VehiculoCreate(VehiculoBase):
    id_cliente: int

# Properties to receive on item update
class VehiculoUpdate(BaseModel):
    placa: Optional[str] = None
    tipo: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año: Optional[int] = None  # Añadido el campo año
    color: Optional[str] = None
    id_cliente: Optional[int] = None
    
    @validator('tipo')
    def validate_tipo(cls, v):
        if v is None:
            return v
        valid_types = ["carro", "moto"]
        if v.lower() not in valid_types:
            raise ValueError(f'Tipo must be one of: {", ".join(valid_types)}')
        return v.lower()
    
    @validator('placa')
    def validate_placa(cls, v):
        if v is None:
            return v
        # Simple validation for Colombian license plates
        if not re.match(r'^[A-Z0-9]{5,7}$', v.upper()):
            raise ValueError('Invalid license plate format')
        return v.upper()
    
    @validator('año')
    def validate_año(cls, v):
        if v is None:
            return v
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

# Properties shared by models stored in DB
class VehiculoInDBBase(VehiculoBase):
    id_vehiculo: int
    id_cliente: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Vehiculo(VehiculoInDBBase):
    pass

# Properties stored in DB
class VehiculoInDB(VehiculoInDBBase):
    pass


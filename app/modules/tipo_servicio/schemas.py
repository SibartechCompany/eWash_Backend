from typing import Optional, List
from pydantic import BaseModel, validator, condecimal
from decimal import Decimal

# Shared properties
class TipoServicioBase(BaseModel):
    nombre: str
    descripcion: str
    precio_base: condecimal(max_digits=10, decimal_places=2, ge=Decimal('0'))
    tipo_vehiculo: str
    
    @validator('tipo_vehiculo')
    def validate_tipo_vehiculo(cls, v):
        valid_types = ["carro", "moto"]
        if v.lower() not in valid_types:
            raise ValueError(f'Tipo vehiculo must be one of: {", ".join(valid_types)}')
        return v.lower()

# Properties to receive on item creation
class TipoServicioCreate(TipoServicioBase):
    pass

# Properties to receive on item update
class TipoServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal('0'))] = None
    tipo_vehiculo: Optional[str] = None
    
    @validator('tipo_vehiculo')
    def validate_tipo_vehiculo(cls, v):
        if v is None:
            return v
        valid_types = ["carro", "moto"]
        if v.lower() not in valid_types:
            raise ValueError(f'Tipo vehiculo must be one of: {", ".join(valid_types)}')
        return v.lower()

# Properties shared by models stored in DB
class TipoServicioInDBBase(TipoServicioBase):
    id_tipo_servicio: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class TipoServicio(TipoServicioInDBBase):
    pass

# Properties stored in DB
class TipoServicioInDB(TipoServicioInDBBase):
    pass

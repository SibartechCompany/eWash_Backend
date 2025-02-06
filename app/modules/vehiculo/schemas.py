from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class VehiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    tipo_vehiculo: str
    id_cliente: UUID
    total_lavados: Optional[int] = 0
    ultima_fecha_lavado: Optional[date] = None

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id_vehiculo: UUID

    class Config:
        from_attributes = True

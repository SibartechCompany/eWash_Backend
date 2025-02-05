# app/modules/user/schemas.py

from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    email: str
    cedula: str

class ClienteCreate(ClienteBase):
    fecha_registro: Optional[date] = None

class Cliente(ClienteBase):
    id_cliente: UUID
    fecha_registro: date

    class Config:
        from_attributes = True


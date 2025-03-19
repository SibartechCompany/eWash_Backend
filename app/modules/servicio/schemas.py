from typing import Optional, List, ClassVar
from pydantic import BaseModel, validator, condecimal
from datetime import datetime
from decimal import Decimal

# Shared properties
class ServicioBase(BaseModel):
    fecha_hora: datetime = datetime.utcnow()
    precio: condecimal(max_digits=10, decimal_places=2, ge=Decimal('0'))
    comentarios: Optional[str] = None

# Properties to receive on item creation
class ServicioCreate(ServicioBase):
    id_vehiculo: int
    id_empleado: int
    id_tipo_servicio: int

# Properties to receive on item update
class ServicioUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    precio: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal('0'))] = None
    comentarios: Optional[str] = None
    id_vehiculo: Optional[int] = None
    id_empleado: Optional[int] = None
    id_tipo_servicio: Optional[int] = None

# Properties shared by models stored in DB
class ServicioInDBBase(ServicioBase):
    id_servicio: int
    id_vehiculo: int
    id_empleado: int
    id_tipo_servicio: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class Servicio(ServicioInDBBase):
    pass

# Properties stored in DB
class ServicioInDB(ServicioInDBBase):
    pass

# Extended Servicio with related data
class ServicioExtended(Servicio):
    from app.modules.vehiculo.schemas import Vehiculo
    from app.modules.empleado.schemas import Empleado
    from app.modules.tipo_servicio.schemas import TipoServicio
    
    vehiculo: Vehiculo
    empleado: Empleado
    tipo_servicio: TipoServicio
    
    Vehiculo: ClassVar[type] = Vehiculo
    Empleado: ClassVar[type] = Empleado
    TipoServicio: ClassVar[type] = TipoServicio

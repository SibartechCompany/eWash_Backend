from pydantic import ConfigDict
from typing import Optional, TYPE_CHECKING
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.vehicle import VehicleType

if TYPE_CHECKING:
    from app.schemas.client import ClientSummary

# Vehicle creation schema
class VehicleCreate(BaseCreate):
    vehicle_type: VehicleType
    plate: str
    model: str
    year: Optional[int] = None
    color: Optional[str] = None
    client_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

# Vehicle update schema
class VehicleUpdate(BaseUpdate):
    vehicle_type: Optional[VehicleType] = None
    plate: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

# Vehicle response schema
class Vehicle(BaseInDB):
    vehicle_type: VehicleType
    plate: str
    model: str
    year: Optional[int]
    color: Optional[str]
    client_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

# Vehicle with client info
class VehicleWithClient(Vehicle):
    client: Optional["ClientSummary"] = None

# Vehicle summary for lists
class VehicleSummary(BaseSchema):
    id: uuid.UUID
    vehicle_type: VehicleType
    plate: str
    model: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True) 
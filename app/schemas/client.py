from pydantic import EmailStr, ConfigDict
from typing import Optional, List
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.schemas.vehicle import Vehicle

# Client creation schema
class ClientCreate(BaseCreate):
    full_name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    organization_id: Optional[uuid.UUID] = None  # Se asigna automáticamente

    model_config = ConfigDict(from_attributes=True)

# Client update schema
class ClientUpdate(BaseUpdate):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

# Client response schema
class Client(BaseInDB):
    full_name: str
    email: Optional[str]
    phone: str
    address: Optional[str]
    organization_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

# Client with vehicles
class ClientWithVehicles(Client):
    vehicles: List[Vehicle] = []

    model_config = ConfigDict(from_attributes=True)

# Client summary for lists
class ClientSummary(BaseSchema):
    id: uuid.UUID
    full_name: str
    phone: str
    email: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True) 
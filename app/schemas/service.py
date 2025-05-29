from pydantic import field_validator
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.service import VehicleType

if TYPE_CHECKING:
    from app.schemas.organization import Organization

# Service creation schema
class ServiceCreate(BaseCreate):
    name: str
    description: Optional[str] = None
    price: Decimal
    duration: int  # Duration in minutes
    vehicle_type: VehicleType
    is_active: bool = True

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('Duration must be greater than 0')
        return v

# Service update schema
class ServiceUpdate(BaseUpdate):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    vehicle_type: Optional[VehicleType] = None
    is_active: Optional[bool] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be greater than 0')
        return v

# Service response schema
class Service(BaseInDB):
    name: str
    description: Optional[str]
    price: Decimal
    duration: int
    vehicle_type: VehicleType
    is_active: bool
    organization_id: uuid.UUID

# Service with organization
class ServiceWithOrganization(Service):
    organization: Optional["Organization"] = None

# Service summary for lists
class ServiceSummary(BaseSchema):
    id: uuid.UUID
    name: str
    price: Decimal
    duration: int
    vehicle_type: VehicleType
    is_active: bool 
from pydantic import validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.order import OrderStatus, PaymentStatus

if TYPE_CHECKING:
    from app.schemas.client import Client
    from app.schemas.vehicle import Vehicle
    from app.schemas.service import Service
    from app.schemas.employee import Employee
    from app.schemas.branch import Branch

# Order creation schema (simplified for frontend)
class OrderCreateSimple(BaseCreate):
    service_id: uuid.UUID
    vehicle_id: uuid.UUID
    assigned_employee_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None
    scheduled_at: Optional[datetime] = None

# Order creation schema (complete)
class OrderCreate(BaseCreate):
    order_number: str
    client_id: uuid.UUID
    vehicle_id: uuid.UUID
    service_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    assigned_employee_id: Optional[uuid.UUID] = None
    total_amount: Decimal
    notes: Optional[str] = None
    scheduled_at: Optional[datetime] = None

# Order update schema
class OrderUpdate(BaseUpdate):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    branch_id: Optional[uuid.UUID] = None
    assigned_employee_id: Optional[uuid.UUID] = None
    total_amount: Optional[Decimal] = None
    notes: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Order response schema
class Order(BaseInDB):
    order_number: str
    status: OrderStatus
    payment_status: PaymentStatus
    total_amount: Decimal
    notes: Optional[str]
    scheduled_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    organization_id: uuid.UUID
    branch_id: Optional[uuid.UUID]
    client_id: uuid.UUID
    vehicle_id: uuid.UUID
    service_id: uuid.UUID
    assigned_employee_id: Optional[uuid.UUID]

# Order with relationships
class OrderWithRelations(Order):
    client: Optional["Client"] = None
    vehicle: Optional["Vehicle"] = None
    service: Optional["Service"] = None
    assigned_employee: Optional["Employee"] = None
    branch: Optional["Branch"] = None

# Order summary for lists
class OrderSummary(BaseSchema):
    id: uuid.UUID
    order_number: str
    status: OrderStatus
    payment_status: PaymentStatus
    total_amount: Decimal
    scheduled_at: Optional[datetime]
    client_id: uuid.UUID
    branch_id: Optional[uuid.UUID]
    is_active: bool 
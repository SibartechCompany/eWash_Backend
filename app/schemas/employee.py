from pydantic import EmailStr, field_validator
from typing import Optional, List, TYPE_CHECKING, Union
from datetime import date, datetime
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.employee import DocumentType, EmployeeStatus

if TYPE_CHECKING:
    from app.schemas.user import User
    from app.schemas.branch import Branch

# Employee creation schema
class EmployeeCreate(BaseCreate):
    full_name: str
    document_type: DocumentType
    document_number: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    position: str
    start_date: Optional[Union[date, str]] = None
    branch_id: Optional[uuid.UUID] = None
    # User creation fields
    password: Optional[str] = None
    role: Optional[str] = None

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('start_date must be in YYYY-MM-DD format')
        return v

# Employee update schema
class EmployeeUpdate(BaseUpdate):
    full_name: Optional[str] = None
    document_type: Optional[DocumentType] = None
    document_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[Union[date, str]] = None
    status: Optional[EmployeeStatus] = None
    branch_id: Optional[uuid.UUID] = None

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('start_date must be in YYYY-MM-DD format')
        return v

# Employee response schema
class Employee(BaseInDB):
    full_name: str
    document_type: DocumentType
    document_number: str
    email: Optional[str]
    phone: str
    address: Optional[str]
    position: str
    start_date: Optional[date] = None
    status: EmployeeStatus
    organization_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None

# Employee with user and branch
class EmployeeWithRelations(Employee):
    user: Optional["User"] = None
    branch: Optional["Branch"] = None

# Employee summary for lists
class EmployeeSummary(BaseSchema):
    id: uuid.UUID
    full_name: str
    position: str
    phone: str
    status: EmployeeStatus
    is_active: bool
    branch_id: Optional[uuid.UUID] = None 
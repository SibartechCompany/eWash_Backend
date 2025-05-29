from pydantic import EmailStr
from typing import Optional
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate

# Branch creation schema
class BranchCreate(BaseCreate):
    name: str
    code: str
    description: Optional[str] = None
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    manager_name: Optional[str] = None
    manager_phone: Optional[str] = None
    is_main: Optional[bool] = False

# Branch update schema
class BranchUpdate(BaseUpdate):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    manager_name: Optional[str] = None
    manager_phone: Optional[str] = None
    is_main: Optional[bool] = None

# Branch response schema
class Branch(BaseInDB):
    name: str
    code: str
    description: Optional[str]
    address: str
    phone: Optional[str]
    email: Optional[str]
    manager_name: Optional[str]
    manager_phone: Optional[str]
    is_main: bool
    organization_id: uuid.UUID

# Branch summary for lists
class BranchSummary(BaseSchema):
    id: uuid.UUID
    name: str
    code: str
    address: str
    is_main: bool
    is_active: bool 
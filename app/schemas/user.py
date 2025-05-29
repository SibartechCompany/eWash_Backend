from pydantic import EmailStr, field_validator
from typing import Optional, TYPE_CHECKING
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.user import UserRole

if TYPE_CHECKING:
    from app.schemas.organization import Organization

# User creation schema
class UserCreate(BaseCreate):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.EMPLOYEE
    organization_id: uuid.UUID
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# User update schema
class UserUpdate(BaseUpdate):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    email_verified: Optional[bool] = None

# User response schema
class User(BaseInDB):
    email: str
    full_name: str
    phone: Optional[str]
    is_superuser: bool
    role: UserRole
    organization_id: uuid.UUID
    email_verified: bool
    supabase_user_id: Optional[str]

# User with organization details
class UserWithOrganization(User):
    organization: Optional["Organization"] = None

# Login schema
class UserLogin(BaseSchema):
    email: EmailStr
    password: str

# Password change schema
class PasswordChange(BaseSchema):
    current_password: str
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v 
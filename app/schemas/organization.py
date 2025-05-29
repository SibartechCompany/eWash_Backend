from pydantic import EmailStr, HttpUrl
from typing import Optional, List
import uuid
from app.schemas.base import BaseSchema, BaseInDB, BaseCreate, BaseUpdate
from app.models.organization import OrganizationType

# Organization creation schema
class OrganizationCreate(BaseCreate):
    name: str
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None
    organization_type: OrganizationType = OrganizationType.BRANCH
    parent_organization_id: Optional[uuid.UUID] = None

# Organization update schema
class OrganizationUpdate(BaseUpdate):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None
    organization_type: Optional[OrganizationType] = None
    parent_organization_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None

# Organization response schema
class Organization(BaseInDB):
    name: str
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    organization_type: OrganizationType
    parent_organization_id: Optional[uuid.UUID]

# Organization with relationships
class OrganizationWithRelations(Organization):
    sub_organizations: List[Organization] = []
    parent_organization: Optional[Organization] = None

# Organization summary for lists
class OrganizationSummary(BaseSchema):
    id: uuid.UUID
    name: str
    organization_type: OrganizationType
    city: Optional[str]
    is_active: bool 
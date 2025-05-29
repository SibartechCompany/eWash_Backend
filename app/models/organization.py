from sqlalchemy import Column, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class OrganizationType(str, enum.Enum):
    MAIN = "main"  # Administradora principal
    BRANCH = "branch"  # Sucursal/sublocal

class Organization(BaseModel):
    __tablename__ = "organizations"
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    legal_name = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True, unique=True)
    
    # Contact information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    # Organization hierarchy
    organization_type = Column(Enum(OrganizationType), default=OrganizationType.BRANCH, nullable=False)
    parent_organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    
    # Relationships
    parent_organization = relationship("Organization", remote_side="Organization.id", back_populates="sub_organizations")
    sub_organizations = relationship("Organization", back_populates="parent_organization")
    
    # Related entities
    users = relationship("User", back_populates="organization")
    clients = relationship("Client", back_populates="organization")
    employees = relationship("Employee", back_populates="organization")
    services = relationship("Service", back_populates="organization")
    orders = relationship("Order", back_populates="organization")
    branches = relationship("Branch", back_populates="organization") 
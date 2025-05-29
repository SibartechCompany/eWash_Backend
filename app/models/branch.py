from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Branch(BaseModel):
    __tablename__ = "branches"
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), nullable=False)  # Código único de la sede
    description = Column(String(500), nullable=True)
    
    # Contact information
    address = Column(String(500), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Manager information
    manager_name = Column(String(255), nullable=True)
    manager_phone = Column(String(20), nullable=True)
    
    # Status
    is_main = Column(Boolean, default=False, nullable=False)  # Sede principal
    
    # Organization relationship
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="branches")
    
    # Related entities
    employees = relationship("Employee", back_populates="branch")
    orders = relationship("Order", back_populates="branch") 
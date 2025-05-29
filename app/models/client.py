from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"
    
    # Personal information
    full_name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    
    # Organization relationship
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="clients")
    
    # Related entities
    vehicles = relationship("Vehicle", back_populates="client", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="client") 
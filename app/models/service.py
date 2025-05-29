from sqlalchemy import Column, String, Integer, Text, Enum, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel

class VehicleType(str, enum.Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"

class Service(BaseModel):
    __tablename__ = "services"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Precio en pesos colombianos
    duration = Column(Integer, nullable=False)  # Duración en minutos
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Foreign key
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="services")
    orders = relationship("Order", back_populates="service")
    order_services = relationship("OrderService", back_populates="service") 
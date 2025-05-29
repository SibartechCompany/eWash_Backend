from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class VehicleType(str, enum.Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"

class Vehicle(BaseModel):
    __tablename__ = "vehicles"
    
    # Vehicle information
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    plate = Column(String(20), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=True)
    color = Column(String(50), nullable=True)
    
    # Client relationship
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="vehicles")
    
    # Related entities
    orders = relationship("Order", back_populates="vehicle") 
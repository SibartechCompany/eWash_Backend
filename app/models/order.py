from sqlalchemy import Column, String, Text, DateTime, Numeric, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum
from datetime import datetime

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    REFUNDED = "refunded"

# Tabla intermedia para la relación many-to-many entre Order y Service
class OrderService(BaseModel):
    __tablename__ = "order_services"
    
    # Foreign keys
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    
    # Service details at time of order
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Precio unitario al momento de la orden
    
    # Relationships
    order = relationship("Order", back_populates="order_services")
    service = relationship("Service", back_populates="order_services")

    class Config:
        from_attributes = True

class Order(BaseModel):
    __tablename__ = "orders"
    
    # Order information
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Dates
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Payment information
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Foreign keys
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    assigned_employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    service = relationship("Service", back_populates="orders")
    vehicle = relationship("Vehicle", back_populates="orders")
    assigned_employee = relationship("Employee", back_populates="orders")
    branch = relationship("Branch", back_populates="orders")
    order_services = relationship("OrderService", back_populates="order", cascade="all, delete-orphan")

    class Config:
        from_attributes = True 
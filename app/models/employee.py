from sqlalchemy import Column, String, Date, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import date

from app.models.base import BaseModel

class DocumentType(str, enum.Enum):
    CC = "CC"  # Cédula de Ciudadanía
    CE = "CE"  # Cédula de Extranjería
    TI = "TI"  # Tarjeta de Identidad
    PP = "PP"  # Pasaporte

class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Employee(BaseModel):
    __tablename__ = "employees"
    
    # Personal information
    full_name = Column(String(255), nullable=False, index=True)
    document_type = Column(Enum(DocumentType), nullable=False)
    document_number = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=True)
    
    # Employment information
    position = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=True, default=date.today)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE, nullable=False)
    
    # Organization relationship
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="employees")
    
    # Branch relationship
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id"), nullable=True)
    branch = relationship("Branch", back_populates="employees")
    
    # User relationship (ahora disponible)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="employee")
    
    # Related entities
    orders = relationship("Order", back_populates="assigned_employee") 
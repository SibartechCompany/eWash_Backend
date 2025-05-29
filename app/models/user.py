from sqlalchemy import Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"  # Administrador del sistema
    ADMIN = "admin"  # Administrador de organización
    MANAGER = "manager"  # Gerente de sucursal
    EMPLOYEE = "employee"  # Empleado
    VIEWER = "viewer"  # Solo lectura

class User(BaseModel):
    __tablename__ = "users"
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # User status and permissions
    is_superuser = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    
    # Organization relationship
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="users")
    
    # Employee relationship (ahora disponible)
    employee = relationship("Employee", back_populates="user", uselist=False)
    
    # Email verification
    email_verified = Column(Boolean, default=False, nullable=False)
    
    # Supabase integration
    supabase_user_id = Column(String(255), nullable=True, unique=True) 
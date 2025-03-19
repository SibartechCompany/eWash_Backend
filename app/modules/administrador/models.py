from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Administrador(Base):
    __tablename__ = "administradores"
    
    id_admin = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, index=True)
    usuario = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    
    # Relationships
    sedes = relationship("Sede", back_populates="administrador")
    
    class Config:
        from_attributes = True

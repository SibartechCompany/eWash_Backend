from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Sede(Base):
    __tablename__ = "sedes"
    
    id_sede = Column(Integer, primary_key=True, index=True)
    id_admin = Column(Integer, ForeignKey("administradores.id_admin"))
    nombre = Column(String, index=True)
    direccion = Column(String)
    telefono = Column(String)
    ciudad = Column(String)
    activa = Column(Boolean, default=True)
    
    # Relationships
    administrador = relationship("Administrador", back_populates="sedes")
    empleados = relationship("Empleado", back_populates="sede")

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date

class Empleado(Base):
    __tablename__ = "empleados"
    
    id_empleado = Column(Integer, primary_key=True, index=True)
    id_sede = Column(Integer, ForeignKey("sedes.id_sede"))
    nombre_completo = Column(String, index=True)
    tipo_documento = Column(String)
    numero_documento = Column(String, unique=True, index=True)
    cargo = Column(String)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)
    direccion = Column(String)
    fecha_inicio = Column(Date, default=date.today)
    estado = Column(String, default="activo")
    
    # Relationships
    sede = relationship("Sede", back_populates="empleados")
    servicios = relationship("Servicio", back_populates="empleado")

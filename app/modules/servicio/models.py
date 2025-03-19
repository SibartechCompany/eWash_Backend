from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Servicio(Base):
    __tablename__ = "servicios"
    
    id_servicio = Column(Integer, primary_key=True, index=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))
    id_empleado = Column(Integer, ForeignKey("empleados.id_empleado"))
    id_tipo_servicio = Column(Integer, ForeignKey("tipos_servicio.id_tipo_servicio"))
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    precio = Column(Numeric(10, 2))
    comentarios = Column(Text, nullable=True)
    
    # Relationships
    vehiculo = relationship("Vehiculo", back_populates="servicios")
    empleado = relationship("Empleado", back_populates="servicios")
    tipo_servicio = relationship("TipoServicio", back_populates="servicios")

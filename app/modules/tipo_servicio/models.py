from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class TipoServicio(Base):
    __tablename__ = "tipos_servicio"
    
    id_tipo_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio_base = Column(Numeric(10, 2))
    tipo_vehiculo = Column(String)  # carro/moto
    
    # Relationships
    servicios = relationship("Servicio", back_populates="tipo_servicio")

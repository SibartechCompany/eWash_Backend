from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, index=True)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)
    direccion = Column(String)
    
    # Relationships
    vehiculos = relationship("Vehiculo", back_populates="cliente")

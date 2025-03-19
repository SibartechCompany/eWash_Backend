from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    
    id_vehiculo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    placa = Column(String, unique=True, index=True)
    tipo = Column(String)  # carro/moto
    marca = Column(String)
    modelo = Column(String)
    año = Column(Integer)  # Añadido el campo año
    color = Column(String)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="vehiculos")
    servicios = relationship("Servicio", back_populates="vehiculo")


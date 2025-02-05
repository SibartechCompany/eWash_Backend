from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.database import Base  # Corrige la ruta de importación
from sqlalchemy.orm import relationship

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    color = Column(String, nullable=False)
    tipo_vehiculo = Column(String, nullable=False)  # carro o moto
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    total_lavados = Column(Integer, default=0)
    ultima_fecha_lavado = Column(Date, nullable=True)

    cliente = relationship("Cliente")

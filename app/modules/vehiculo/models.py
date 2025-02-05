from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    placa = Column(String, unique=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    color = Column(String, nullable=False)
    tipo_vehiculo = Column(String, nullable=False)  # carro o moto
    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id_cliente"))
    total_lavados = Column(Integer, default=0)
    ultima_fecha_lavado = Column(Date, nullable=True)

    cliente = relationship("Cliente")

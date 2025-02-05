from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)

class Empleado(Base):
    __tablename__ = "empleados"

    id_empleado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # lavador, supervisor

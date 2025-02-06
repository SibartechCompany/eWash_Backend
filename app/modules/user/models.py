from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente: str = Column(UUID(as_uuid=True), primary_key=True,
                             default=uuid.uuid4, index=True)
    nombre: str = Column(String, nullable=False)
    apellido: str = Column(String, nullable=False)
    telefono: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    document_type: str = Column(String, nullable=False)
    cedula: int = Column(String, unique=True, nullable=False)
    fecha_registro: str = Column(Date, nullable=False)


class Empleado(Base):
    __tablename__ = "empleado"

    id_empleado = Column(UUID(as_uuid=True), primary_key=True,
                         default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # lavador, supervisor

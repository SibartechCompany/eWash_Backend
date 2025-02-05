from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)

class Empleado(Base):
    __tablename__ = "empleados"

    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # lavador, supervisor

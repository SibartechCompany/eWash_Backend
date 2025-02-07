import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Persona(Base):
    __tablename__ = "persona"

    id_persona = Column(UUID(as_uuid=True), primary_key=True,
                             default=uuid.uuid4, index=True)
    nombre= Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono= Column(String, nullable=False)
    email= Column(String, unique=True, nullable=False)

     # Relaciones
    empleado = relationship("Empleado", back_populates="persona", uselist=False)
    cliente = relationship("Cliente", back_populates="persona", uselist=False)

# Tabla específica: Empleado


class Empleado(Base):
    __tablename__ = "empleado"
    id_empleado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_persona = Column(UUID(as_uuid=True), ForeignKey(
        "persona.id_persona"))
    id_rol = Column(UUID(as_uuid=True), ForeignKey(
        "role.id_role"))
    # Por ejemplo, "lavador", "supervisor"

    

    # Relación inversa
    rol = relationship("Role", back_populates="role")
    persona = relationship("Persona", back_populates="empleado")


# Tabla específica: Cliente
class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4, index=True)
    id_persona = Column(UUID(as_uuid=True), ForeignKey(
        "persona.id_persona"))
    # Por ejemplo, "DNI", "Pasaporte"
    document_type = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)

    # Relación inversa
    persona = relationship("Persona", back_populates="cliente")

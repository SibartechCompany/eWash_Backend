from sqlalchemy import Column, Date, String, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid


class OrdenServicio(Base):
    __tablename__ = "orden_servicio"

    id_orden = Column(UUID(as_uuid=True), primary_key=True,
                      default=uuid.uuid4, index=True)
    id_vehiculo = Column(UUID(as_uuid=True),
                         ForeignKey("vehiculos.id_vehiculo"))
    id_empleado = Column(UUID(as_uuid=True),
                         ForeignKey("empleados.id_empleado"))
    fecha_orden = Column(Date, nullable=False)
    # pendiente, en proceso, completado
    estado = Column(String, nullable=False)
    total_cobro = Column(DECIMAL, nullable=False)

    vehiculo = relationship("Vehiculo")
    empleado = relationship("Empleado")

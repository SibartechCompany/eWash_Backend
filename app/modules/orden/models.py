from sqlalchemy import Column, Integer, Date, String, ForeignKey, DECIMAL
from app.core.database import Base  # Corrige la ruta de importación
from sqlalchemy.orm import relationship

class OrdenServicio(Base):
    __tablename__ = "ordenes_servicio"

    id_orden = Column(Integer, primary_key=True, index=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))
    id_empleado = Column(Integer, ForeignKey("empleados.id_empleado"))
    fecha_orden = Column(Date, nullable=False)
    estado = Column(String, nullable=False)  # pendiente, en proceso, completado
    total_cobro = Column(DECIMAL, nullable=False)

    vehiculo = relationship("Vehiculo")
    empleado = relationship("Empleado")

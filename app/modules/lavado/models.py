from sqlalchemy import Column, Integer, Date, String, ForeignKey, DECIMAL
from app.core.database import Base
from sqlalchemy.orm import relationship

class TipoLavado(Base):
    __tablename__ = "tipos_lavado"

    id_tipo_lavado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # básico, premium, completo
    precio = Column(DECIMAL, nullable=False)
    duracion_estimada = Column(String, nullable=False)

class HistorialLavado(Base):
    __tablename__ = "historial_lavado"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_orden = Column(Integer, ForeignKey("ordenes_servicio.id_orden"))
    id_tipo_lavado = Column(Integer, ForeignKey("tipos_lavado.id_tipo_lavado"))
    fecha_lavado = Column(Date, nullable=False)
    observaciones = Column(String, nullable=True)
    estado_lavado = Column(String, nullable=False)  # iniciado, terminado, inspeccionado

    orden = relationship("OrdenServicio")
    tipo_lavado = relationship("TipoLavado")

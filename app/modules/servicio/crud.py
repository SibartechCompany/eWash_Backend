from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.servicio.models import Servicio
from app.modules.servicio.schemas import ServicioCreate, ServicioUpdate

def get_by_id(db: Session, id: int) -> Optional[Servicio]:
    return db.query(Servicio).filter(Servicio.id_servicio == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Servicio]:
    return db.query(Servicio).offset(skip).limit(limit).all()

def get_by_vehiculo(
    db: Session, *, vehiculo_id: int, skip: int = 0, limit: int = 100
) -> List[Servicio]:
    return db.query(Servicio).filter(Servicio.id_vehiculo == vehiculo_id).offset(skip).limit(limit).all()

def get_by_empleado(
    db: Session, *, empleado_id: int, skip: int = 0, limit: int = 100
) -> List[Servicio]:
    return db.query(Servicio).filter(Servicio.id_empleado == empleado_id).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: ServicioCreate) -> Servicio:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Servicio(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Servicio, obj_in: ServicioUpdate
) -> Servicio:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Servicio:
    obj = db.query(Servicio).get(id)
    db.delete(obj)
    db.commit()
    return obj

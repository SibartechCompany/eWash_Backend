from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.tipo_servicio.models import TipoServicio
from app.modules.tipo_servicio.schemas import TipoServicioCreate, TipoServicioUpdate

def get_by_id(db: Session, id: int) -> Optional[TipoServicio]:
    return db.query(TipoServicio).filter(TipoServicio.id_tipo_servicio == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[TipoServicio]:
    return db.query(TipoServicio).offset(skip).limit(limit).all()

def get_by_tipo_vehiculo(
    db: Session, *, tipo_vehiculo: str, skip: int = 0, limit: int = 100
) -> List[TipoServicio]:
    return db.query(TipoServicio).filter(TipoServicio.tipo_vehiculo == tipo_vehiculo).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: TipoServicioCreate) -> TipoServicio:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = TipoServicio(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: TipoServicio, obj_in: TipoServicioUpdate
) -> TipoServicio:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> TipoServicio:
    obj = db.query(TipoServicio).get(id)
    db.delete(obj)
    db.commit()
    return obj

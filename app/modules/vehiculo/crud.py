from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.vehiculo.models import Vehiculo
from app.modules.vehiculo.schemas import VehiculoCreate, VehiculoUpdate

def get_by_id(db: Session, id: int) -> Optional[Vehiculo]:
    return db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id).first()

def get_by_placa(db: Session, placa: str) -> Optional[Vehiculo]:
    return db.query(Vehiculo).filter(Vehiculo.placa == placa).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Vehiculo]:
    return db.query(Vehiculo).offset(skip).limit(limit).all()

def get_by_cliente(
    db: Session, *, cliente_id: int, skip: int = 0, limit: int = 100
) -> List[Vehiculo]:
    return db.query(Vehiculo).filter(Vehiculo.id_cliente == cliente_id).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: VehiculoCreate) -> Vehiculo:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Vehiculo(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Vehiculo, obj_in: VehiculoUpdate
) -> Vehiculo:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Vehiculo:
    obj = db.query(Vehiculo).get(id)
    db.delete(obj)
    db.commit()
    return obj

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.empleado.models import Empleado
from app.modules.empleado.schemas import EmpleadoCreate, EmpleadoUpdate

def get_by_id(db: Session, id: int) -> Optional[Empleado]:
    return db.query(Empleado).filter(Empleado.id_empleado == id).first()

def get_by_documento(db: Session, numero_documento: str) -> Optional[Empleado]:
    return db.query(Empleado).filter(Empleado.numero_documento == numero_documento).first()

def get_by_email(db: Session, email: str) -> Optional[Empleado]:
    return db.query(Empleado).filter(Empleado.email == email).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Empleado]:
    return db.query(Empleado).offset(skip).limit(limit).all()

def get_by_sede(
    db: Session, *, sede_id: int, skip: int = 0, limit: int = 100
) -> List[Empleado]:
    return db.query(Empleado).filter(Empleado.id_sede == sede_id).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: EmpleadoCreate) -> Empleado:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Empleado(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Empleado, obj_in: EmpleadoUpdate
) -> Empleado:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Empleado:
    obj = db.query(Empleado).get(id)
    db.delete(obj)
    db.commit()
    return obj

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.sede.models import Sede
from app.modules.sede.schemas import SedeCreate, SedeUpdate

def get_by_id(db: Session, id: int) -> Optional[Sede]:
    return db.query(Sede).filter(Sede.id_sede == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Sede]:
    return db.query(Sede).offset(skip).limit(limit).all()

def get_by_admin(
    db: Session, *, admin_id: int, skip: int = 0, limit: int = 100
) -> List[Sede]:
    return db.query(Sede).filter(Sede.id_admin == admin_id).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: SedeCreate) -> Sede:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Sede(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Sede, obj_in: SedeUpdate
) -> Sede:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Sede:
    obj = db.query(Sede).get(id)
    db.delete(obj)
    db.commit()
    return obj

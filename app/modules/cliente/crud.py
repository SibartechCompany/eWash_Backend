from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.cliente.models import Cliente
from app.modules.cliente.schemas import ClienteCreate, ClienteUpdate

def get_by_id(db: Session, id: int) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.id_cliente == id).first()

def get_by_email(db: Session, email: str) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.email == email).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: ClienteCreate) -> Cliente:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Cliente(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Cliente, obj_in: ClienteUpdate
) -> Cliente:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Cliente:
    obj = db.query(Cliente).get(id)
    db.delete(obj)
    db.commit()
    return obj

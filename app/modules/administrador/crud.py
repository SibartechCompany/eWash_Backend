from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.core.security import get_password_hash, verify_password
from app.modules.administrador.models import Administrador
from app.modules.administrador.schemas import AdministradorCreate, AdministradorUpdate

def get_by_id(db: Session, id: int) -> Optional[Administrador]:
    return db.query(Administrador).filter(Administrador.id_admin == id).first()

def get_by_email(db: Session, email: str) -> Optional[Administrador]:
    return db.query(Administrador).filter(Administrador.email == email).first()

def get_by_username(db: Session, username: str) -> Optional[Administrador]:
    return db.query(Administrador).filter(Administrador.usuario == username).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Administrador]:
    return db.query(Administrador).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: AdministradorCreate) -> Administrador:
    db_obj = Administrador(
        nombre_completo=obj_in.nombre_completo,
        usuario=obj_in.usuario,
        email=obj_in.email,
        telefono=obj_in.telefono,
        password=get_password_hash(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Administrador, obj_in: AdministradorUpdate
) -> Administrador:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["password"] = hashed_password
        
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, id: int) -> Administrador:
    obj = db.query(Administrador).get(id)
    db.delete(obj)
    db.commit()
    return obj

def authenticate(db: Session, *, username: str, password: str) -> Optional[Administrador]:
    user = get_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def count(db: Session) -> int:
    return db.query(Administrador).count()



from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.administrador import crud, schemas
from app.core.exceptions import NotFoundError, DuplicateError

router = APIRouter()

@router.get("/", response_model=List[schemas.Administrador])
def read_administradores(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all administrators.
    """
    administradores = crud.get_multi(db, skip=skip, limit=limit)
    return administradores

@router.post("/", response_model=schemas.Administrador)
def create_administrador(
    *,
    db: Session = Depends(get_db),
    administrador_in: schemas.AdministradorCreate,
    current_user: schemas.AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new administrator.
    """
    administrador = crud.get_by_email(db, email=administrador_in.email)
    if administrador:
        raise DuplicateError(
            detail="The administrator with this email already exists in the system"
        )
    
    username_exists = crud.get_by_username(db, username=administrador_in.usuario)
    if username_exists:
        raise DuplicateError(
            detail="The administrator with this username already exists in the system"
        )
    
    administrador = crud.create(db, obj_in=administrador_in)
    return administrador

@router.get("/{administrador_id}", response_model=schemas.Administrador)
def read_administrador(
    *,
    db: Session = Depends(get_db),
    administrador_id: int,
    current_user: schemas.AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get administrator by ID.
    """
    administrador = crud.get_by_id(db, id=administrador_id)
    if not administrador:
        raise NotFoundError(detail="Administrator not found")
    return administrador

@router.put("/{administrador_id}", response_model=schemas.Administrador)
def update_administrador(
    *,
    db: Session = Depends(get_db),
    administrador_id: int,
    administrador_in: schemas.AdministradorUpdate,
    current_user: schemas.AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update an administrator.
    """
    administrador = crud.get_by_id(db, id=administrador_id)
    if not administrador:
        raise NotFoundError(detail="Administrator not found")
    
    if administrador_in.email and administrador_in.email != administrador.email:
        existing = crud.get_by_email(db, email=administrador_in.email)
        if existing:
            raise DuplicateError(
                detail="The administrator with this email already exists in the system"
            )
    
    if administrador_in.usuario and administrador_in.usuario != administrador.usuario:
        existing = crud.get_by_username(db, username=administrador_in.usuario)
        if existing:
            raise DuplicateError(
                detail="The administrator with this username already exists in the system"
            )
    
    administrador = crud.update(db, db_obj=administrador, obj_in=administrador_in)
    return administrador

@router.delete("/{administrador_id}", response_model=schemas.Administrador)
def delete_administrador(
    *,
    db: Session = Depends(get_db),
    administrador_id: int,
    current_user: schemas.AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete an administrator.
    """
    administrador = crud.get_by_id(db, id=administrador_id)
    if not administrador:
        raise NotFoundError(detail="Administrator not found")
    administrador = crud.delete(db, id=administrador_id)
    return administrador

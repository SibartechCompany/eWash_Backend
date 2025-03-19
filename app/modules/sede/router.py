from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.sede import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/", response_model=List[schemas.Sede])
def read_sedes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all branches.
    """
    sedes = crud.get_multi(db, skip=skip, limit=limit)
    return sedes

@router.post("/", response_model=schemas.Sede)
def create_sede(
    *,
    db: Session = Depends(get_db),
    sede_in: schemas.SedeCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new branch.
    """
    sede = crud.create(db, obj_in=sede_in)
    return sede

@router.get("/{sede_id}", response_model=schemas.Sede)
def read_sede(
    *,
    db: Session = Depends(get_db),
    sede_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get branch by ID.
    """
    sede = crud.get_by_id(db, id=sede_id)
    if not sede:
        raise NotFoundError(detail="Branch not found")
    return sede

@router.put("/{sede_id}", response_model=schemas.Sede)
def update_sede(
    *,
    db: Session = Depends(get_db),
    sede_id: int,
    sede_in: schemas.SedeUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a branch.
    """
    sede = crud.get_by_id(db, id=sede_id)
    if not sede:
        raise NotFoundError(detail="Branch not found")
    sede = crud.update(db, db_obj=sede, obj_in=sede_in)
    return sede

@router.delete("/{sede_id}", response_model=schemas.Sede)
def delete_sede(
    *,
    db: Session = Depends(get_db),
    sede_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete a branch.
    """
    sede = crud.get_by_id(db, id=sede_id)
    if not sede:
        raise NotFoundError(detail="Branch not found")
    sede = crud.delete(db, id=sede_id)
    return sede

@router.get("/by-admin/{admin_id}", response_model=List[schemas.Sede])
def read_sedes_by_admin(
    *,
    db: Session = Depends(get_db),
    admin_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve branches by admin ID.
    """
    sedes = crud.get_by_admin(db, admin_id=admin_id, skip=skip, limit=limit)
    return sedes

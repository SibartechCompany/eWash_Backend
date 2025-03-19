from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.tipo_servicio import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/", response_model=List[schemas.TipoServicio])
def read_tipos_servicio(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all service types.
    """
    tipos_servicio = crud.get_multi(db, skip=skip, limit=limit)
    return tipos_servicio

@router.post("/", response_model=schemas.TipoServicio)
def create_tipo_servicio(
    *,
    db: Session = Depends(get_db),
    tipo_servicio_in: schemas.TipoServicioCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new service type.
    """
    tipo_servicio = crud.create(db, obj_in=tipo_servicio_in)
    return tipo_servicio

@router.get("/{tipo_servicio_id}", response_model=schemas.TipoServicio)
def read_tipo_servicio(
    *,
    db: Session = Depends(get_db),
    tipo_servicio_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get service type by ID.
    """
    tipo_servicio = crud.get_by_id(db, id=tipo_servicio_id)
    if not tipo_servicio:
        raise NotFoundError(detail="Service type not found")
    return tipo_servicio

@router.put("/{tipo_servicio_id}", response_model=schemas.TipoServicio)
def update_tipo_servicio(
    *,
    db: Session = Depends(get_db),
    tipo_servicio_id: int,
    tipo_servicio_in: schemas.TipoServicioUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a service type.
    """
    tipo_servicio = crud.get_by_id(db, id=tipo_servicio_id)
    if not tipo_servicio:
        raise NotFoundError(detail="Service type not found")
    tipo_servicio = crud.update(db, db_obj=tipo_servicio, obj_in=tipo_servicio_in)
    return tipo_servicio

@router.delete("/{tipo_servicio_id}", response_model=schemas.TipoServicio)
def delete_tipo_servicio(
    *,
    db: Session = Depends(get_db),
    tipo_servicio_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete a service type.
    """
    tipo_servicio = crud.get_by_id(db, id=tipo_servicio_id)
    if not tipo_servicio:
        raise NotFoundError(detail="Service type not found")
    tipo_servicio = crud.delete(db, id=tipo_servicio_id)
    return tipo_servicio

@router.get("/by-tipo-vehiculo/{tipo_vehiculo}", response_model=List[schemas.TipoServicio])
def read_tipos_servicio_by_tipo_vehiculo(
    *,
    db: Session = Depends(get_db),
    tipo_vehiculo: str,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve service types by vehicle type.
    """
    tipos_servicio = crud.get_by_tipo_vehiculo(db, tipo_vehiculo=tipo_vehiculo, skip=skip, limit=limit)
    return tipos_servicio

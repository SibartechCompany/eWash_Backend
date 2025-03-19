from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.servicio import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/", response_model=List[schemas.Servicio])
def read_servicios(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all services.
    """
    servicios = crud.get_multi(db, skip=skip, limit=limit)
    return servicios

@router.post("/", response_model=schemas.Servicio)
def create_servicio(
    *,
    db: Session = Depends(get_db),
    servicio_in: schemas.ServicioCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new service.
    """
    servicio = crud.create(db, obj_in=servicio_in)
    return servicio

@router.get("/{servicio_id}", response_model=schemas.Servicio)
def read_servicio(
    *,
    db: Session = Depends(get_db),
    servicio_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get service by ID.
    """
    servicio = crud.get_by_id(db, id=servicio_id)
    if not servicio:
        raise NotFoundError(detail="Service not found")
    return servicio

@router.put("/{servicio_id}", response_model=schemas.Servicio)
def update_servicio(
    *,
    db: Session = Depends(get_db),
    servicio_id: int,
    servicio_in: schemas.ServicioUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a service.
    """
    servicio = crud.get_by_id(db, id=servicio_id)
    if not servicio:
        raise NotFoundError(detail="Service not found")
    servicio = crud.update(db, db_obj=servicio, obj_in=servicio_in)
    return servicio

@router.delete("/{servicio_id}", response_model=schemas.Servicio)
def delete_servicio(
    *,
    db: Session = Depends(get_db),
    servicio_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete a service.
    """
    servicio = crud.get_by_id(db, id=servicio_id)
    if not servicio:
        raise NotFoundError(detail="Service not found")
    servicio = crud.delete(db, id=servicio_id)
    return servicio

@router.get("/by-vehiculo/{vehiculo_id}", response_model=List[schemas.Servicio])
def read_servicios_by_vehiculo(
    *,
    db: Session = Depends(get_db),
    vehiculo_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve services by vehicle ID.
    """
    servicios = crud.get_by_vehiculo(db, vehiculo_id=vehiculo_id, skip=skip, limit=limit)
    return servicios

@router.get("/by-empleado/{empleado_id}", response_model=List[schemas.Servicio])
def read_servicios_by_empleado(
    *,
    db: Session = Depends(get_db),
    empleado_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve services by employee ID.
    """
    servicios = crud.get_by_empleado(db, empleado_id=empleado_id, skip=skip, limit=limit)
    return servicios

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.vehiculo import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError, DuplicateError

router = APIRouter()

@router.get("/", response_model=List[schemas.Vehiculo])
def read_vehiculos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all vehicles.
    """
    vehiculos = crud.get_multi(db, skip=skip, limit=limit)
    return vehiculos

@router.post("/", response_model=schemas.Vehiculo)
def create_vehiculo(
    *,
    db: Session = Depends(get_db),
    vehiculo_in: schemas.VehiculoCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new vehicle.
    """
    vehiculo = crud.get_by_placa(db, placa=vehiculo_in.placa)
    if vehiculo:
        raise DuplicateError(
            detail="The vehicle with this license plate already exists in the system"
        )
    
    vehiculo = crud.create(db, obj_in=vehiculo_in)
    return vehiculo

@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
def read_vehiculo(
    *,
    db: Session = Depends(get_db),
    vehiculo_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get vehicle by ID.
    """
    vehiculo = crud.get_by_id(db, id=vehiculo_id)
    if not vehiculo:
        raise NotFoundError(detail="Vehicle not found")
    return vehiculo

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def update_vehiculo(
    *,
    db: Session = Depends(get_db),
    vehiculo_id: int,
    vehiculo_in: schemas.VehiculoUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a vehicle.
    """
    vehiculo = crud.get_by_id(db, id=vehiculo_id)
    if not vehiculo:
        raise NotFoundError(detail="Vehicle not found")
    
    if vehiculo_in.placa and vehiculo_in.placa != vehiculo.placa:
        existing = crud.get_by_placa(db, placa=vehiculo_in.placa)
        if existing:
            raise DuplicateError(
                detail="The vehicle with this license plate already exists in the system"
            )
    
    vehiculo = crud.update(db, db_obj=vehiculo, obj_in=vehiculo_in)
    return vehiculo

@router.delete("/{vehiculo_id}", response_model=schemas.Vehiculo)
def delete_vehiculo(
    *,
    db: Session = Depends(get_db),
    vehiculo_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete a vehicle.
    """
    vehiculo = crud.get_by_id(db, id=vehiculo_id)
    if not vehiculo:
        raise NotFoundError(detail="Vehicle not found")
    vehiculo = crud.delete(db, id=vehiculo_id)
    return vehiculo

@router.get("/by-cliente/{cliente_id}", response_model=List[schemas.Vehiculo])
def read_vehiculos_by_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve vehicles by client ID.
    """
    vehiculos = crud.get_by_cliente(db, cliente_id=cliente_id, skip=skip, limit=limit)
    return vehiculos

@router.get("/by-placa/{placa}", response_model=schemas.Vehiculo)
def read_vehiculo_by_placa(
    *,
    db: Session = Depends(get_db),
    placa: str,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get vehicle by license plate.
    """
    vehiculo = crud.get_by_placa(db, placa=placa)
    if not vehiculo:
        raise NotFoundError(detail="Vehicle not found")
    return vehiculo

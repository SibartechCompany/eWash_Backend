from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.empleado import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError, DuplicateError

router = APIRouter()

@router.get("/", response_model=List[schemas.Empleado])
def read_empleados(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all employees.
    """
    empleados = crud.get_multi(db, skip=skip, limit=limit)
    return empleados

@router.post("/", response_model=schemas.Empleado)
def create_empleado(
    *,
    db: Session = Depends(get_db),
    empleado_in: schemas.EmpleadoCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new employee.
    """
    # Check if employee with same document already exists
    empleado = crud.get_by_documento(db, numero_documento=empleado_in.numero_documento)
    if empleado:
        raise DuplicateError(
            detail="An employee with this document number already exists in the system"
        )
    
    # Check if employee with same email already exists
    empleado = crud.get_by_email(db, email=empleado_in.email)
    if empleado:
        raise DuplicateError(
            detail="An employee with this email already exists in the system"
        )
    
    empleado = crud.create(db, obj_in=empleado_in)
    return empleado

@router.get("/{empleado_id}", response_model=schemas.Empleado)
def read_empleado(
    *,
    db: Session = Depends(get_db),
    empleado_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get employee by ID.
    """
    empleado = crud.get_by_id(db, id=empleado_id)
    if not empleado:
        raise NotFoundError(detail="Employee not found")
    return empleado

@router.put("/{empleado_id}", response_model=schemas.Empleado)
def update_empleado(
    *,
    db: Session = Depends(get_db),
    empleado_id: int,
    empleado_in: schemas.EmpleadoUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update an employee.
    """
    empleado = crud.get_by_id(db, id=empleado_id)
    if not empleado:
        raise NotFoundError(detail="Employee not found")
    
    # Check if updating to an existing document number
    if empleado_in.numero_documento and empleado_in.numero_documento != empleado.numero_documento:
        existing = crud.get_by_documento(db, numero_documento=empleado_in.numero_documento)
        if existing:
            raise DuplicateError(
                detail="An employee with this document number already exists in the system"
            )
    
    # Check if updating to an existing email
    if empleado_in.email and empleado_in.email != empleado.email:
        existing = crud.get_by_email(db, email=empleado_in.email)
        if existing:
            raise DuplicateError(
                detail="An employee with this email already exists in the system"
            )
    
    empleado = crud.update(db, db_obj=empleado, obj_in=empleado_in)
    return empleado

@router.delete("/{empleado_id}", response_model=schemas.Empleado)
def delete_empleado(
    *,
    db: Session = Depends(get_db),
    empleado_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete an employee.
    """
    empleado = crud.get_by_id(db, id=empleado_id)
    if not empleado:
        raise NotFoundError(detail="Employee not found")
    empleado = crud.delete(db, id=empleado_id)
    return empleado

@router.get("/by-sede/{sede_id}", response_model=List[schemas.Empleado])
def read_empleados_by_sede(
    *,
    db: Session = Depends(get_db),
    sede_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve employees by branch ID.
    """
    empleados = crud.get_by_sede(db, sede_id=sede_id, skip=skip, limit=limit)
    return empleados

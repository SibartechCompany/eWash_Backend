from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_db
from app.modules.cliente import crud, schemas
from app.modules.administrador.schemas import AdministradorInDB
from app.core.exceptions import NotFoundError, DuplicateError

router = APIRouter()

@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all clients.
    """
    clientes = crud.get_multi(db, skip=skip, limit=limit)
    return clientes

@router.post("/", response_model=schemas.Cliente)
def create_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_in: schemas.ClienteCreate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Create new client.
    """
    cliente = crud.get_by_email(db, email=cliente_in.email)
    if cliente:
        raise DuplicateError(
            detail="The client with this email already exists in the system"
        )
    
    cliente = crud.create(db, obj_in=cliente_in)
    return cliente

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get client by ID.
    """
    cliente = crud.get_by_id(db, id=cliente_id)
    if not cliente:
        raise NotFoundError(detail="Client not found")
    return cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    cliente_in: schemas.ClienteUpdate,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update a client.
    """
    cliente = crud.get_by_id(db, id=cliente_id)
    if not cliente:
        raise NotFoundError(detail="Client not found")
    
    if cliente_in.email and cliente_in.email != cliente.email:
        existing = crud.get_by_email(db, email=cliente_in.email)
        if existing:
            raise DuplicateError(
                detail="The client with this email already exists in the system"
            )
    
    cliente = crud.update(db, db_obj=cliente, obj_in=cliente_in)
    return cliente

@router.delete("/{cliente_id}", response_model=schemas.Cliente)
def delete_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    current_user: AdministradorInDB = Depends(get_current_active_user),
) -> Any:
    """
    Delete a client.
    """
    cliente = crud.get_by_id(db, id=cliente_id)
    if not cliente:
        raise NotFoundError(detail="Client not found")
    cliente = crud.delete(db, id=cliente_id)
    return cliente

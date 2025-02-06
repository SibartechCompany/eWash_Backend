from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.user import schemas, models
from datetime import date
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar si el teléfono ya existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.telefono == cliente.telefono).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El número de teléfono ya está registrado")
    
    # Verificar si la cédula ya existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cedula == cliente.cedula).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    
    if not cliente.fecha_registro:
        cliente.fecha_registro = date.today()
    db_cliente = models.Cliente(
        nombre=cliente.nombre,
        telefono=cliente.telefono,
        email=cliente.email,
        cedula=cliente.cedula,
        fecha_registro=cliente.fecha_registro
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}", response_model=schemas.Cliente)
def delete_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: UUID, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar si el email ya existe y pertenece a otro cliente
    db_cliente_email = db.query(models.Cliente).filter(models.Cliente.email == cliente.email, models.Cliente.id_cliente != cliente_id).first()
    if db_cliente_email:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar si el teléfono ya existe y pertenece a otro cliente
    db_cliente_telefono = db.query(models.Cliente).filter(models.Cliente.telefono == cliente.telefono, models.Cliente.id_cliente != cliente_id).first()
    if db_cliente_telefono:
        raise HTTPException(status_code=400, detail="El número de teléfono ya está registrado")
    
    # Verificar si la cédula ya existe y pertenece a otro cliente
    db_cliente_cedula = db.query(models.Cliente).filter(models.Cliente.cedula == cliente.cedula, models.Cliente.id_cliente != cliente_id).first()
    if db_cliente_cedula:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    
    db_cliente.nombre = cliente.nombre
    db_cliente.telefono = cliente.telefono
    db_cliente.email = cliente.email
    db_cliente.cedula = cliente.cedula
    if cliente.fecha_registro:
        db_cliente.fecha_registro = cliente.fecha_registro
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

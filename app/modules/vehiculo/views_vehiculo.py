from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.vehiculo import schemas, models
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=schemas.Vehiculo)
def create_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if db_vehiculo:
        raise HTTPException(status_code=400, detail="La placa ya está registrada")
    
    db_vehiculo = models.Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.delete("/{vehiculo_id}", response_model=schemas.Vehiculo)
def delete_vehiculo(vehiculo_id: UUID, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id_vehiculo == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    db.delete(db_vehiculo)
    db.commit()
    return db_vehiculo

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def update_vehiculo(vehiculo_id: UUID, vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id_vehiculo == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    db_vehiculo.placa = vehiculo.placa
    db_vehiculo.marca = vehiculo.marca
    db_vehiculo.modelo = vehiculo.modelo
    db_vehiculo.color = vehiculo.color
    db_vehiculo.tipo_vehiculo = vehiculo.tipo_vehiculo
    db_vehiculo.id_cliente = vehiculo.id_cliente
    db_vehiculo.total_lavados = vehiculo.total_lavados
    db_vehiculo.ultima_fecha_lavado = vehiculo.ultima_fecha_lavado
    
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

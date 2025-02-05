from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import Base, engine
from app.modules.user import models as user_models
from app.modules.vehiculo import models as vehiculo_models
from app.modules.orden import models as orden_models
from app.modules.lavado import models as lavado_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)  # Crea las tablas en la BD
    yield  # Aquí podrías añadir código para limpiar recursos si fuera necesario

app = FastAPI(lifespan=lifespan)

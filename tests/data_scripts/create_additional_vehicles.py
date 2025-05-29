#!/usr/bin/env python3
"""
Script para crear vehículos adicionales para los clientes existentes
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.client import Client
from app.models.vehicle import Vehicle, VehicleType
from app.crud.base import CRUDBase
from sqlalchemy import select

# CRUD instances
crud_vehicle = CRUDBase(Vehicle)

async def create_additional_vehicles():
    """Crear vehículos adicionales para los clientes existentes"""
    
    async with AsyncSessionLocal() as db:
        try:
            # 1. Buscar la organización admin
            print("🔍 Buscando organización admin...")
            
            org_query = select(Organization).where(Organization.email == "admin@ewash.com")
            org_result = await db.execute(org_query)
            organization = org_result.scalar_one_or_none()
            
            if not organization:
                print("❌ No se encontró la organización admin")
                return
            
            print(f"✅ Organización encontrada: {organization.name}")
            
            # 2. Buscar clientes sin vehículos
            clients_query = select(Client).where(Client.organization_id == organization.id)
            clients_result = await db.execute(clients_query)
            clients = clients_result.scalars().all()
            
            print(f"📊 Clientes encontrados: {len(clients)}")
            
            # 3. Crear vehículos para los clientes que no tienen
            vehicles_data = [
                {
                    "plate": "ABC123",
                    "model": "Toyota Corolla",
                    "year": 2020,
                    "color": "Blanco",
                    "vehicle_type": VehicleType.CAR,
                    "client_name": "Juan Carlos Pérez"
                },
                {
                    "plate": "DEF456", 
                    "model": "Honda Civic",
                    "year": 2019,
                    "color": "Negro",
                    "vehicle_type": VehicleType.CAR,
                    "client_name": "María González"
                },
                {
                    "plate": "GHI789",
                    "model": "Yamaha FZ",
                    "year": 2021,
                    "color": "Azul",
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "client_name": "Carlos Rodríguez"
                },
                {
                    "plate": "JKL012",
                    "model": "Chevrolet Spark",
                    "year": 2018,
                    "color": "Rojo",
                    "vehicle_type": VehicleType.CAR,
                    "client_name": "Ana Martínez"
                },
                {
                    "plate": "MNO345",
                    "model": "Kawasaki Ninja",
                    "year": 2022,
                    "color": "Verde",
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "client_name": "Luis Hernández"
                }
            ]
            
            created_count = 0
            for vehicle_data in vehicles_data:
                # Buscar el cliente por nombre
                client = next((c for c in clients if c.full_name == vehicle_data["client_name"]), None)
                
                if client:
                    # Verificar si ya tiene vehículos
                    existing_vehicles_query = select(Vehicle).where(Vehicle.client_id == client.id)
                    existing_vehicles_result = await db.execute(existing_vehicles_query)
                    existing_vehicles = existing_vehicles_result.scalars().all()
                    
                    if len(existing_vehicles) == 0:
                        # Crear el vehículo
                        vehicle_create_data = {
                            "plate": vehicle_data["plate"],
                            "model": vehicle_data["model"],
                            "year": vehicle_data["year"],
                            "color": vehicle_data["color"],
                            "vehicle_type": vehicle_data["vehicle_type"],
                            "client_id": client.id
                        }
                        
                        vehicle = await crud_vehicle.create(db, obj_in=vehicle_create_data)
                        print(f"✅ Vehículo creado: {vehicle.model} - {vehicle.plate} para {client.full_name}")
                        created_count += 1
                    else:
                        print(f"⚠️ Cliente {client.full_name} ya tiene {len(existing_vehicles)} vehículo(s)")
                else:
                    print(f"❌ Cliente no encontrado: {vehicle_data['client_name']}")
            
            print(f"\n📈 Total de vehículos creados: {created_count}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Creando vehículos adicionales...")
    asyncio.run(create_additional_vehicles()) 
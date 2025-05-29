#!/usr/bin/env python3
"""
Script para crear servicios de ejemplo en eWash
Ejecutar: python create_sample_services.py
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.service import Service, VehicleType
from app.crud.base import CRUDBase
from sqlalchemy import select
from decimal import Decimal

# CRUD instance
crud_service = CRUDBase(Service)

async def create_sample_services():
    """Crear servicios de ejemplo"""
    
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
            
            # 2. Verificar si ya existen servicios
            existing_query = select(Service).where(Service.organization_id == organization.id)
            existing_result = await db.execute(existing_query)
            existing_services = existing_result.scalars().all()
            
            if existing_services:
                print(f"✅ Ya existen {len(existing_services)} servicios")
                for service in existing_services:
                    print(f"   - {service.name} ({service.vehicle_type.value}): ${service.price}")
                return
            
            # 3. Crear servicios de ejemplo
            print("🚗 Creando servicios de ejemplo...")
            
            services_data = [
                # Servicios para automóviles
                {
                    "name": "Lavado Básico Auto",
                    "description": "Lavado exterior, aspirado interior y limpieza de vidrios",
                    "price": Decimal("15000"),
                    "duration": 30,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Premium Auto",
                    "description": "Lavado completo con encerado y protección de neumáticos",
                    "price": Decimal("25000"),
                    "duration": 45,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Deluxe Auto",
                    "description": "Servicio completo con detallado interior y exterior",
                    "price": Decimal("40000"),
                    "duration": 90,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                # Servicios para motocicletas
                {
                    "name": "Lavado Básico Moto",
                    "description": "Lavado exterior y secado completo",
                    "price": Decimal("10000"),
                    "duration": 20,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Premium Moto",
                    "description": "Lavado completo con encerado y limpieza de cadena",
                    "price": Decimal("18000"),
                    "duration": 35,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Deluxe Moto",
                    "description": "Servicio completo con detallado y protección de plásticos",
                    "price": Decimal("25000"),
                    "duration": 50,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                }
            ]
            
            created_services = []
            for service_data in services_data:
                service = await crud_service.create(db, obj_in=service_data)
                created_services.append(service)
                print(f"✅ Servicio creado: {service.name} - ${service.price}")
            
            print(f"\n🎉 ¡{len(created_services)} servicios creados exitosamente!")
            print("=" * 60)
            
            # Mostrar resumen por tipo
            car_services = [s for s in created_services if s.vehicle_type == VehicleType.CAR]
            moto_services = [s for s in created_services if s.vehicle_type == VehicleType.MOTORCYCLE]
            
            print(f"🚗 Servicios para automóviles: {len(car_services)}")
            for service in car_services:
                print(f"   - {service.name}: ${service.price} ({service.duration} min)")
            
            print(f"\n🏍️ Servicios para motocicletas: {len(moto_services)}")
            for service in moto_services:
                print(f"   - {service.name}: ${service.price} ({service.duration} min)")
            
            print("=" * 60)
            print("💡 Ahora puedes ver estos servicios en el frontend")
            
        except Exception as e:
            print(f"❌ Error al crear servicios: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de servicios de ejemplo...")
    asyncio.run(create_sample_services()) 
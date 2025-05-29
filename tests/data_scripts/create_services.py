#!/usr/bin/env python3
"""
Script para crear servicios de ejemplo en eWash
Ejecutar: python create_services.py
"""

import asyncio
import sys
import os
from decimal import Decimal

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.service import Service, VehicleType
from app.crud.base import CRUDBase
from sqlalchemy import select

# CRUD instance
crud_service = CRUDBase(Service)

async def create_services():
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
            existing_services_query = select(Service).where(Service.organization_id == organization.id)
            existing_services_result = await db.execute(existing_services_query)
            existing_services = existing_services_result.scalars().all()
            
            if len(existing_services) >= 6:
                print(f"✅ Ya existen {len(existing_services)} servicios")
                return
            
            # 3. Crear servicios de ejemplo
            print("🚗 Creando servicios de ejemplo...")
            
            services_data = [
                # Servicios para automóviles
                {
                    "name": "Lavado Básico Auto",
                    "description": "Lavado exterior completo con jabón y encerado básico",
                    "price": Decimal("15000"),
                    "duration": 30,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Premium Auto",
                    "description": "Lavado completo exterior e interior con aspirado y aromatización",
                    "price": Decimal("25000"),
                    "duration": 45,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Detallado Auto",
                    "description": "Lavado completo con encerado, limpieza de motor y detallado interior",
                    "price": Decimal("40000"),
                    "duration": 90,
                    "vehicle_type": VehicleType.CAR,
                    "is_active": True,
                    "organization_id": organization.id
                },
                # Servicios para motocicletas
                {
                    "name": "Lavado Básico Moto",
                    "description": "Lavado exterior completo para motocicleta",
                    "price": Decimal("8000"),
                    "duration": 20,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Premium Moto",
                    "description": "Lavado completo con encerado y limpieza de cadena",
                    "price": Decimal("12000"),
                    "duration": 30,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                },
                {
                    "name": "Lavado Detallado Moto",
                    "description": "Lavado completo con encerado, limpieza de motor y cadena",
                    "price": Decimal("18000"),
                    "duration": 45,
                    "vehicle_type": VehicleType.MOTORCYCLE,
                    "is_active": True,
                    "organization_id": organization.id
                }
            ]
            
            created_services = []
            for service_data in services_data:
                service = await crud_service.create(db, obj_in=service_data)
                created_services.append(service)
                print(f"✅ Servicio creado: {service.name} - {service.vehicle_type.value} - ${service.price}")
            
            print(f"\n🎉 ¡{len(created_services)} servicios creados exitosamente!")
            print("=" * 60)
            print("💡 Ahora puedes ver los servicios en el frontend")
            
        except Exception as e:
            print(f"❌ Error al crear servicios: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de servicios...")
    asyncio.run(create_services()) 
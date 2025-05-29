#!/usr/bin/env python3
"""
Script para probar la creación de órdenes
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.client import Client
from app.models.vehicle import Vehicle
from app.models.service import Service
from app.models.user import User as UserModel
from app.api.v1.endpoints.orders import create_order
from app.schemas.order import OrderCreateSimple
from sqlalchemy import select

async def test_order_creation():
    """Probar la creación de órdenes"""
    
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
            
            # 2. Buscar un usuario real de la organización
            user_query = select(UserModel).where(UserModel.organization_id == organization.id)
            user_result = await db.execute(user_query)
            user = user_result.scalar_one_or_none()
            
            if not user:
                print("❌ No se encontró ningún usuario en la organización")
                return
            
            print(f"✅ Usuario encontrado: {user.full_name}")
            
            # 3. Buscar un servicio
            service_query = select(Service).where(Service.organization_id == organization.id)
            service_result = await db.execute(service_query)
            service = service_result.scalars().first()
            
            if not service:
                print("❌ No se encontró ningún servicio")
                return
            
            print(f"✅ Servicio encontrado: {service.name}")
            
            # 4. Buscar un vehículo
            vehicle_query = select(Vehicle).join(Client).where(Client.organization_id == organization.id)
            vehicle_result = await db.execute(vehicle_query)
            vehicle = vehicle_result.scalars().first()
            
            if not vehicle:
                print("❌ No se encontró ningún vehículo")
                return
            
            print(f"✅ Vehículo encontrado: {vehicle.model} - {vehicle.plate}")
            
            # 5. Crear una orden de prueba
            print("\n🧪 Probando creación de orden...")
            
            order_data = OrderCreateSimple(
                service_id=service.id,
                vehicle_id=vehicle.id,
                notes="Orden de prueba creada desde script"
            )
            
            order = await create_order(
                db=db,
                order_in=order_data,
                current_user=user
            )
            
            print(f"✅ Orden creada exitosamente:")
            print(f"   📋 Número: {order.order_number}")
            print(f"   💰 Total: ${order.total_amount}")
            print(f"   📝 Estado: {order.status}")
            print(f"   🚗 Vehículo ID: {order.vehicle_id}")
            print(f"   🔧 Servicio ID: {order.service_id}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Probando creación de órdenes...")
    asyncio.run(test_order_creation()) 
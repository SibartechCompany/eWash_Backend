#!/usr/bin/env python3
"""
Script para crear órdenes simples sin fechas complejas
Ejecutar: python create_simple_orders.py
"""

import asyncio
import sys
import os
from decimal import Decimal

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.client import Client
from app.models.vehicle import Vehicle
from app.models.service import Service
from app.models.order import Order, OrderStatus
from app.crud.base import CRUDBase
from sqlalchemy import select

# CRUD instance
crud_order = CRUDBase(Order)

async def create_simple_orders():
    """Crear órdenes simples"""
    
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
            
            # 2. Obtener servicios
            services_query = select(Service).where(Service.organization_id == organization.id)
            services_result = await db.execute(services_query)
            services = services_result.scalars().all()
            
            if not services:
                print("❌ No hay servicios disponibles")
                return
            
            # 3. Obtener vehículos con información del cliente
            vehicles_query = select(Vehicle, Client).join(Client).where(Client.organization_id == organization.id)
            vehicles_result = await db.execute(vehicles_query)
            vehicles_with_clients = vehicles_result.all()
            
            if not vehicles_with_clients:
                print("❌ No hay vehículos disponibles")
                return
            
            # 4. Verificar órdenes existentes
            existing_orders_query = select(Order).where(Order.organization_id == organization.id)
            existing_orders_result = await db.execute(existing_orders_query)
            existing_orders = existing_orders_result.scalars().all()
            
            if len(existing_orders) >= 5:
                print(f"✅ Ya existen {len(existing_orders)} órdenes")
                return
            
            # 5. Crear órdenes simples
            print("📋 Creando órdenes simples...")
            
            orders_data = []
            for i in range(3):
                vehicle, client = vehicles_with_clients[i % len(vehicles_with_clients)]
                service = services[i % len(services)]
                
                status = [OrderStatus.PENDING, OrderStatus.IN_PROGRESS, OrderStatus.COMPLETED][i]
                
                order_data = {
                    "order_number": f"ORD-{i+1:04d}",
                    "service_id": service.id,
                    "vehicle_id": vehicle.id,
                    "client_id": client.id,
                    "status": status,
                    "total_amount": service.price,
                    "notes": f"Orden de ejemplo #{i+1}",
                    "organization_id": organization.id
                }
                orders_data.append(order_data)
            
            created_orders = []
            for order_data in orders_data:
                order = await crud_order.create(db, obj_in=order_data)
                created_orders.append(order)
                print(f"✅ Orden creada: {order.order_number} - {order.status.value} - ${order.total_amount}")
            
            print(f"\n🎉 ¡{len(created_orders)} órdenes creadas exitosamente!")
            print("=" * 60)
            print("💡 Ahora el dashboard debería mostrar datos reales")
            
        except Exception as e:
            print(f"❌ Error al crear órdenes: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de órdenes simples...")
    asyncio.run(create_simple_orders()) 
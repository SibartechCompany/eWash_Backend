#!/usr/bin/env python3
"""
Script para crear datos de ejemplo completos en eWash
Ejecutar: python create_sample_data.py
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.client import Client
from app.models.vehicle import Vehicle, VehicleType
from app.models.service import Service
from app.models.order import Order, OrderStatus
from app.crud.base import CRUDBase
from sqlalchemy import select

# CRUD instances
crud_client = CRUDBase(Client)
crud_vehicle = CRUDBase(Vehicle)
crud_order = CRUDBase(Order)

async def create_sample_data():
    """Crear datos de ejemplo completos"""
    
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
            
            # 2. Verificar si ya existen clientes
            existing_clients_query = select(Client).where(Client.organization_id == organization.id)
            existing_clients_result = await db.execute(existing_clients_query)
            existing_clients = existing_clients_result.scalars().all()
            
            if len(existing_clients) >= 5:
                print(f"✅ Ya existen {len(existing_clients)} clientes")
            else:
                # 3. Crear clientes de ejemplo
                print("👥 Creando clientes de ejemplo...")
                
                clients_data = [
                    {
                        "full_name": "Juan Carlos Pérez",
                        "email": "juan.perez@email.com",
                        "phone": "+57 300 123 4567",
                        "address": "Calle 123 #45-67, Bogotá",
                        "organization_id": organization.id
                    },
                    {
                        "full_name": "María González",
                        "email": "maria.gonzalez@email.com", 
                        "phone": "+57 301 234 5678",
                        "address": "Carrera 45 #12-34, Bogotá",
                        "organization_id": organization.id
                    },
                    {
                        "full_name": "Carlos Rodríguez",
                        "email": "carlos.rodriguez@email.com",
                        "phone": "+57 302 345 6789",
                        "address": "Avenida 68 #23-45, Bogotá",
                        "organization_id": organization.id
                    },
                    {
                        "full_name": "Ana Martínez",
                        "email": "ana.martinez@email.com",
                        "phone": "+57 303 456 7890",
                        "address": "Calle 72 #34-56, Bogotá",
                        "organization_id": organization.id
                    },
                    {
                        "full_name": "Luis Hernández",
                        "email": "luis.hernandez@email.com",
                        "phone": "+57 304 567 8901",
                        "address": "Carrera 15 #56-78, Bogotá",
                        "organization_id": organization.id
                    }
                ]
                
                created_clients = []
                for client_data in clients_data:
                    client = await crud_client.create(db, obj_in=client_data)
                    created_clients.append(client)
                    print(f"✅ Cliente creado: {client.full_name}")
                
                # 4. Crear vehículos para los clientes
                print("🚗 Creando vehículos de ejemplo...")
                
                vehicles_data = [
                    {
                        "plate": "ABC123",
                        "model": "Toyota Corolla",
                        "year": 2020,
                        "color": "Blanco",
                        "vehicle_type": VehicleType.CAR,
                        "client_id": created_clients[0].id
                    },
                    {
                        "plate": "DEF456",
                        "model": "Honda Civic",
                        "year": 2019,
                        "color": "Negro",
                        "vehicle_type": VehicleType.CAR,
                        "client_id": created_clients[1].id
                    },
                    {
                        "plate": "GHI789",
                        "model": "Yamaha FZ",
                        "year": 2021,
                        "color": "Azul",
                        "vehicle_type": VehicleType.MOTORCYCLE,
                        "client_id": created_clients[2].id
                    },
                    {
                        "plate": "JKL012",
                        "model": "Chevrolet Spark",
                        "year": 2018,
                        "color": "Rojo",
                        "vehicle_type": VehicleType.CAR,
                        "client_id": created_clients[3].id
                    },
                    {
                        "plate": "MNO345",
                        "model": "Kawasaki Ninja",
                        "year": 2022,
                        "color": "Verde",
                        "vehicle_type": VehicleType.MOTORCYCLE,
                        "client_id": created_clients[4].id
                    }
                ]
                
                created_vehicles = []
                for vehicle_data in vehicles_data:
                    vehicle = await crud_vehicle.create(db, obj_in=vehicle_data)
                    created_vehicles.append(vehicle)
                    print(f"✅ Vehículo creado: {vehicle.model} - {vehicle.plate}")
            
            # 5. Obtener servicios existentes
            services_query = select(Service).where(Service.organization_id == organization.id)
            services_result = await db.execute(services_query)
            services = services_result.scalars().all()
            
            if not services:
                print("❌ No hay servicios disponibles")
                return
            
            # 6. Verificar si ya existen órdenes
            existing_orders_query = select(Order).where(Order.organization_id == organization.id)
            existing_orders_result = await db.execute(existing_orders_query)
            existing_orders = existing_orders_result.scalars().all()
            
            if len(existing_orders) >= 10:
                print(f"✅ Ya existen {len(existing_orders)} órdenes")
            else:
                # 7. Obtener clientes y vehículos
                all_clients_query = select(Client).where(Client.organization_id == organization.id)
                all_clients_result = await db.execute(all_clients_query)
                all_clients = all_clients_result.scalars().all()
                
                all_vehicles_query = select(Vehicle).join(Client).where(Client.organization_id == organization.id)
                all_vehicles_result = await db.execute(all_vehicles_query)
                all_vehicles = all_vehicles_result.scalars().all()
                
                if not all_clients or not all_vehicles:
                    print("❌ No hay clientes o vehículos disponibles")
                    return
                
                # 8. Crear órdenes de ejemplo
                print("📋 Creando órdenes de ejemplo...")
                
                # Crear órdenes de los últimos 30 días
                base_date = datetime.now()
                
                orders_data = []
                for i in range(10):
                    # Fecha aleatoria en los últimos 30 días
                    days_ago = i * 3
                    order_date = base_date - timedelta(days=days_ago)
                    
                    # Seleccionar cliente, vehículo y servicio
                    client = all_clients[i % len(all_clients)]
                    vehicle = all_vehicles[i % len(all_vehicles)]
                    service = services[i % len(services)]
                    
                    # Estado de la orden
                    if i < 3:
                        status = OrderStatus.COMPLETED
                        completed_date = order_date + timedelta(hours=1)
                    elif i < 6:
                        status = OrderStatus.IN_PROGRESS
                        completed_date = None
                    else:
                        status = OrderStatus.PENDING
                        completed_date = None
                    
                    order_data = {
                        "order_number": f"ORD-{i+1:04d}",
                        "service_id": service.id,
                        "vehicle_id": vehicle.id,
                        "status": status,
                        "total_amount": service.price,
                        "notes": f"Orden de ejemplo #{i+1}",
                        "organization_id": organization.id
                    }
                    
                    # Solo agregar fechas si no son None
                    if completed_date:
                        order_data["completed_at"] = completed_date
                    
                    orders_data.append(order_data)
                
                created_orders = []
                for order_data in orders_data:
                    order = await crud_order.create(db, obj_in=order_data)
                    created_orders.append(order)
                    print(f"✅ Orden creada: {order.order_number} - {order.status.value} - ${order.total_amount}")
            
            print(f"\n🎉 ¡Datos de ejemplo creados exitosamente!")
            print("=" * 60)
            print(f"👥 Clientes: {len(all_clients) if 'all_clients' in locals() else 'Ya existían'}")
            print(f"🚗 Vehículos: {len(all_vehicles) if 'all_vehicles' in locals() else 'Ya existían'}")
            print(f"📋 Órdenes: {len(existing_orders) + len(created_orders) if 'created_orders' in locals() else len(existing_orders)}")
            print("=" * 60)
            print("💡 Ahora el dashboard debería mostrar datos reales")
            
        except Exception as e:
            print(f"❌ Error al crear datos: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de datos de ejemplo...")
    asyncio.run(create_sample_data()) 
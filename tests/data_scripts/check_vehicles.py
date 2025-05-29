#!/usr/bin/env python3
"""
Script para verificar vehículos en la base de datos
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
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def check_vehicles():
    """Verificar vehículos en la base de datos"""
    
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
            
            # 2. Buscar clientes con sus vehículos
            clients_query = select(Client).options(
                selectinload(Client.vehicles)
            ).where(Client.organization_id == organization.id)
            clients_result = await db.execute(clients_query)
            clients = clients_result.scalars().all()
            
            print(f"\n📊 Clientes encontrados: {len(clients)}")
            print("=" * 60)
            
            total_vehicles = 0
            for client in clients:
                print(f"👤 Cliente: {client.full_name}")
                print(f"   🆔 ID: {client.id}")
                print(f"   📞 Teléfono: {client.phone}")
                
                if client.vehicles:
                    print(f"   🚗 Vehículos ({len(client.vehicles)}):")
                    for vehicle in client.vehicles:
                        if vehicle.is_active:
                            print(f"      • {vehicle.model} ({vehicle.plate})")
                            print(f"        Tipo: {vehicle.vehicle_type}")
                            print(f"        Color: {vehicle.color}")
                            print(f"        Año: {vehicle.year}")
                            print(f"        ID: {vehicle.id}")
                            total_vehicles += 1
                else:
                    print("   🚗 Sin vehículos registrados")
                
                print("-" * 40)
            
            print(f"\n📈 Total de vehículos activos: {total_vehicles}")
            
            # 3. Verificar vehículos directamente
            vehicles_query = select(Vehicle).where(Vehicle.is_active == True)
            vehicles_result = await db.execute(vehicles_query)
            all_vehicles = vehicles_result.scalars().all()
            
            print(f"🔍 Verificación directa - Total vehículos activos: {len(all_vehicles)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Verificando vehículos en la base de datos...")
    asyncio.run(check_vehicles()) 
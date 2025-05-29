#!/usr/bin/env python3
"""
Script para probar el endpoint de vehículos
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
from app.models.user import User as UserModel
from app.api.v1.endpoints.vehicles import read_vehicles
from sqlalchemy import select

async def test_vehicles_endpoint():
    """Probar el endpoint de vehículos"""
    
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
            
            # 3. Buscar clientes
            clients_query = select(Client).where(Client.organization_id == organization.id)
            clients_result = await db.execute(clients_query)
            clients = clients_result.scalars().all()
            
            print(f"📊 Clientes encontrados: {len(clients)}")
            
            # 4. Probar el endpoint sin filtro de cliente
            print("\n🧪 Probando endpoint sin filtro de cliente...")
            pagination = {"skip": 0, "limit": 100}
            
            vehicles_all = await read_vehicles(
                db=db,
                pagination=pagination,
                current_user=user,
                client_id=None
            )
            
            print(f"✅ Vehículos obtenidos (sin filtro): {len(vehicles_all)}")
            for vehicle in vehicles_all:
                print(f"   • {vehicle.model} - {vehicle.plate} (Cliente ID: {vehicle.client_id})")
            
            # 5. Probar el endpoint con filtro de cliente
            if clients:
                test_client = clients[0]
                print(f"\n🧪 Probando endpoint con filtro de cliente: {test_client.full_name}")
                
                vehicles_filtered = await read_vehicles(
                    db=db,
                    pagination=pagination,
                    current_user=user,
                    client_id=str(test_client.id)
                )
                
                print(f"✅ Vehículos obtenidos (con filtro): {len(vehicles_filtered)}")
                for vehicle in vehicles_filtered:
                    print(f"   • {vehicle.model} - {vehicle.plate}")
                
                # 6. Probar con otro cliente
                if len(clients) > 1:
                    test_client2 = clients[1]
                    print(f"\n🧪 Probando endpoint con otro cliente: {test_client2.full_name}")
                    
                    vehicles_filtered2 = await read_vehicles(
                        db=db,
                        pagination=pagination,
                        current_user=user,
                        client_id=str(test_client2.id)
                    )
                    
                    print(f"✅ Vehículos obtenidos (cliente 2): {len(vehicles_filtered2)}")
                    for vehicle in vehicles_filtered2:
                        print(f"   • {vehicle.model} - {vehicle.plate}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Probando endpoint de vehículos...")
    asyncio.run(test_vehicles_endpoint()) 
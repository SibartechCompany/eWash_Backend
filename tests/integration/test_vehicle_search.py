#!/usr/bin/env python3
"""
Script para probar la búsqueda de vehículos por placa
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.user import User as UserModel
from app.api.v1.endpoints.vehicles import search_vehicle_by_plate
from sqlalchemy import select

async def test_vehicle_search():
    """Probar la búsqueda de vehículos por placa"""
    
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
            
            # 3. Probar búsqueda por placa
            test_plates = ["JXY23F", "ABC123", "DEF456", "XYZ999"]
            
            for plate in test_plates:
                print(f"\n🔍 Buscando vehículo con placa: {plate}")
                try:
                    vehicle = await search_vehicle_by_plate(
                        plate=plate,
                        db=db,
                        current_user=user
                    )
                    
                    print(f"✅ Vehículo encontrado:")
                    print(f"   🚗 Modelo: {vehicle.model}")
                    print(f"   🏷️ Placa: {vehicle.plate}")
                    print(f"   🎨 Color: {vehicle.color}")
                    print(f"   📅 Año: {vehicle.year}")
                    print(f"   🔧 Tipo: {vehicle.vehicle_type}")
                    
                    if hasattr(vehicle, 'client') and vehicle.client:
                        print(f"   👤 Cliente: {vehicle.client.full_name}")
                        print(f"   📞 Teléfono: {vehicle.client.phone}")
                    
                except Exception as e:
                    print(f"❌ No encontrado: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Probando búsqueda de vehículos por placa...")
    asyncio.run(test_vehicle_search()) 
#!/usr/bin/env python3
"""
Script para verificar clientes en la base de datos
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.client import Client
from sqlalchemy import select

async def check_clients():
    """Verificar clientes en la base de datos"""
    
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
            
            # 2. Buscar clientes
            clients_query = select(Client).where(Client.organization_id == organization.id)
            clients_result = await db.execute(clients_query)
            clients = clients_result.scalars().all()
            
            print(f"\n📊 Clientes encontrados: {len(clients)}")
            print("=" * 50)
            
            for client in clients:
                print(f"👤 {client.full_name}")
                print(f"   📧 {client.email}")
                print(f"   📞 {client.phone}")
                print(f"   🏠 {client.address}")
                print(f"   🆔 {client.id}")
                print(f"   ✅ Activo: {client.is_active}")
                print("-" * 30)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Verificando clientes en la base de datos...")
    asyncio.run(check_clients()) 
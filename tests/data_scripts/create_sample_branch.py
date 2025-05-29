#!/usr/bin/env python3
"""
Script para crear sede de ejemplo en eWash
Ejecutar: python create_sample_branch.py
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.branch import Branch
from app.crud.base import CRUDBase
from sqlalchemy import select

# CRUD instance
crud_branch = CRUDBase(Branch)

async def create_sample_branch():
    """Crear sede de ejemplo"""
    
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
            
            # 2. Verificar si ya existen sedes
            existing_query = select(Branch).where(Branch.organization_id == organization.id)
            existing_result = await db.execute(existing_query)
            existing_branches = existing_result.scalars().all()
            
            if existing_branches:
                print(f"✅ Ya existen {len(existing_branches)} sedes")
                for branch in existing_branches:
                    main_text = " (Principal)" if branch.is_main else ""
                    print(f"   - {branch.name}{main_text}: {branch.address}")
                return
            
            # 3. Crear sede principal de ejemplo
            print("🏢 Creando sede principal de ejemplo...")
            
            branch_data = {
                "name": "eWash Sede Principal",
                "code": "MAIN001",
                "description": "Sede principal del lavadero eWash",
                "address": "Av. Principal 123, Bogotá, Colombia",
                "phone": "+57 1 234 5678",
                "email": "principal@ewash.com",
                "manager_name": "Carlos Rodríguez",
                "manager_phone": "+57 300 123 4567",
                "is_main": True,
                "organization_id": organization.id
            }
            
            branch = await crud_branch.create(db, obj_in=branch_data)
            print(f"✅ Sede creada: {branch.name}")
            
            print(f"\n🎉 ¡Sede principal creada exitosamente!")
            print("=" * 50)
            print(f"🏢 Nombre: {branch.name}")
            print(f"📍 Dirección: {branch.address}")
            print(f"📞 Teléfono: {branch.phone}")
            print(f"👨‍💼 Gerente: {branch.manager_name}")
            print(f"🔑 Código: {branch.code}")
            print("=" * 50)
            print("💡 Ahora puedes ver esta sede en el selector de sedes")
            
        except Exception as e:
            print(f"❌ Error al crear sede: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de sede de ejemplo...")
    asyncio.run(create_sample_branch()) 
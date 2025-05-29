#!/usr/bin/env python3
"""
Script para crear usuario admin en eWash
Ejecutar: python create_admin.py
"""

import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal, init_db
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationCreate
from app.schemas.user import UserCreate
from app.crud.organization import organization
from app.crud.user import user
from app.core.security import get_password_hash

async def create_admin_user():
    """Crear usuario admin y organización principal"""
    
    # Inicializar base de datos
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            # 1. Crear organización principal
            print("🏢 Creando organización principal...")
            
            org_data = OrganizationCreate(
                name="eWash Administración",
                type="main",
                address="Av. Principal 123, Ciudad",
                phone="+1234567890",
                email="admin@ewash.com",
                tax_id="12345678901"
            )
            
            # Verificar si ya existe
            existing_org = await organization.get_by_email(db, email="admin@ewash.com")
            if existing_org:
                print("✅ Organización ya existe")
                organization_obj = existing_org
            else:
                organization_obj = await organization.create(db, obj_in=org_data)
                print(f"✅ Organización creada: {organization_obj.name}")
            
            # 2. Crear usuario admin
            print("👤 Creando usuario admin...")
            
            # Verificar si ya existe
            existing_user = await user.get_by_email(db, email="admin@ewash.com")
            if existing_user:
                print("✅ Usuario admin ya existe")
                print(f"📧 Email: {existing_user.email}")
                print(f"🔑 Contraseña: admin123")
                return
            
            user_data = UserCreate(
                email="admin@ewash.com",
                password="admin123",
                full_name="Administrador eWash",
                role="super_admin",
                organization_id=str(organization_obj.id)
            )
            
            user_obj = await user.create(db, obj_in=user_data)
            print(f"✅ Usuario admin creado: {user_obj.email}")
            
            # 3. Mostrar credenciales
            print("\n🎉 ¡Usuario admin creado exitosamente!")
            print("=" * 50)
            print(f"📧 Email: {user_obj.email}")
            print(f"🔑 Contraseña: admin123")
            print(f"👑 Rol: {user_obj.role}")
            print(f"🏢 Organización: {organization_obj.name}")
            print("=" * 50)
            print("\n💡 Puedes usar estas credenciales para hacer login en el frontend")
            
        except Exception as e:
            print(f"❌ Error al crear usuario admin: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de usuario admin...")
    asyncio.run(create_admin_user()) 
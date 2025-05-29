-- Script para crear tabla branches y agregar columnas necesarias
-- Ejecutar en Supabase SQL Editor

-- 1. Crear tabla branches
CREATE TABLE IF NOT EXISTS branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    description VARCHAR(500),
    address VARCHAR(500) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    manager_name VARCHAR(255),
    manager_phone VARCHAR(20),
    is_main BOOLEAN DEFAULT FALSE NOT NULL,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Crear índices para branches
CREATE INDEX IF NOT EXISTS idx_branches_organization_id ON branches(organization_id);
CREATE INDEX IF NOT EXISTS idx_branches_code ON branches(code);
CREATE INDEX IF NOT EXISTS idx_branches_name ON branches(name);

-- 3. Crear índice único para código por organización
CREATE UNIQUE INDEX IF NOT EXISTS idx_branches_code_org ON branches(code, organization_id) WHERE is_active = TRUE;

-- 4. Agregar columna branch_id a employees (si no existe)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='employees' AND column_name='branch_id') THEN
        ALTER TABLE employees ADD COLUMN branch_id UUID REFERENCES branches(id) ON DELETE SET NULL;
    END IF;
END $$;

-- 5. Agregar columna branch_id a orders (si no existe)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='branch_id') THEN
        ALTER TABLE orders ADD COLUMN branch_id UUID REFERENCES branches(id) ON DELETE SET NULL;
    END IF;
END $$;

-- 6. Crear índices para las nuevas columnas
CREATE INDEX IF NOT EXISTS idx_employees_branch_id ON employees(branch_id);
CREATE INDEX IF NOT EXISTS idx_orders_branch_id ON orders(branch_id);

-- 7. Comentarios para documentar
COMMENT ON TABLE branches IS 'Sedes o sucursales de las organizaciones';
COMMENT ON COLUMN branches.code IS 'Código único de la sede dentro de la organización';
COMMENT ON COLUMN branches.is_main IS 'Indica si es la sede principal';
COMMENT ON COLUMN employees.branch_id IS 'Referencia a la sede donde trabaja el empleado';
COMMENT ON COLUMN orders.branch_id IS 'Referencia a la sede donde se realizó la orden'; 
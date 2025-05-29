-- Script para crear usuario admin en eWash
-- Ejecutar en el SQL Editor de Supabase

-- 1. Crear organización principal
INSERT INTO organizations
    (
    id,
    name,
    type,
    status,
    address,
    phone,
    email,
    tax_id,
    created_at,
    updated_at
    )
VALUES
    (
        gen_random_uuid(),
        'eWash Administración',
        'main',
        'active',
        'Av. Principal 123, Ciudad',
        '+1234567890',
        'admin@ewash.com',
        '12345678901',
        NOW(),
        NOW()
)
ON CONFLICT DO NOTHING;

-- 2. Obtener el ID de la organización (para usar en el siguiente paso)
-- Nota: Reemplaza 'organization_id_here' con el ID real de la organización creada

-- 3. Crear usuario admin
INSERT INTO users
    (
    id,
    email,
    password_hash,
    full_name,
    role,
    status,
    organization_id,
    is_verified,
    created_at,
    updated_at
    )
VALUES
    (
        gen_random_uuid(),
        'admin@ewash.com',
        '$2b$12$LQv3c1yqBwlVHpPjrCyeNOSBKtdXRrVRAVqyr4/P7QFXzjgb9Uy7m', -- password: admin123
        'Administrador eWash',
        'super_admin',
        'active',
        (SELECT id
        FROM organizations
        WHERE email = 'admin@ewash.com'
LIMIT 1),
    true,
    NOW
(),
    NOW
()
) ON CONFLICT
(email) DO NOTHING;

-- 4. Verificar que se creó correctamente
SELECT
    u.id,
    u.email,
    u.full_name,
    u.role,
    u.status,
    o.name as organization_name
FROM users u
    JOIN organizations o ON u.organization_id = o.id
WHERE u.email = 'admin@ewash.com'; 
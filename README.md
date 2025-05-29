# 🚗 eWash Backend API

Backend API para el sistema de gestión de lavaderos de autos eWash, construido con FastAPI, SQLAlchemy y PostgreSQL (Supabase).

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python con soporte async
- **PostgreSQL** - Base de datos relacional (Supabase)
- **Pydantic** - Validación de datos y serialización
- **JWT** - Autenticación basada en tokens
- **Uvicorn** - Servidor ASGI de alto rendimiento

## 📁 Estructura del Proyecto

```
app/
├── main.py                    # Punto de entrada de la aplicación
├── core/                      # Configuraciones centrales
│   ├── config.py              # Configuración con Pydantic Settings
│   ├── security.py            # Autenticación JWT y seguridad
│   └── database.py            # Conexión a base de datos
├── api/                       # Rutas de la API
│   ├── router.py              # Router principal
│   └── v1/                    # Versión 1 de la API
│       ├── dependencies.py    # Dependencias reutilizables
│       └── endpoints/         # Endpoints por dominio
│           ├── auth.py        # Autenticación
│           ├── users.py       # Usuarios
│           ├── organizations.py # Organizaciones
│           ├── clients.py     # Clientes
│           ├── vehicles.py    # Vehículos
│           ├── employees.py   # Empleados
│           ├── services.py    # Servicios
│           └── orders.py      # Órdenes
├── models/                    # Modelos SQLAlchemy
│   ├── base.py               # Modelo base
│   ├── organization.py       # Organizaciones (multi-tenant)
│   ├── user.py              # Usuarios
│   ├── client.py            # Clientes
│   ├── vehicle.py           # Vehículos
│   ├── employee.py          # Empleados
│   ├── service.py           # Servicios
│   └── order.py             # Órdenes
├── schemas/                  # Esquemas Pydantic
│   ├── base.py              # Esquemas base
│   ├── user.py              # Esquemas de usuario
│   ├── organization.py      # Esquemas de organización
│   ├── client.py            # Esquemas de cliente
│   ├── vehicle.py           # Esquemas de vehículo
│   ├── service.py           # Esquemas de servicio
│   └── token.py             # Esquemas de autenticación
├── crud/                     # Operaciones de base de datos
│   ├── base.py              # CRUD base
│   ├── user.py              # CRUD de usuarios
│   ├── organization.py      # CRUD de organizaciones
│   └── client.py            # CRUD de clientes
└── utils/                    # Utilidades
    └── helpers.py           # Funciones auxiliares
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- PostgreSQL (o cuenta de Supabase)

### Instalación

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd eWash_Backend
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
   Crear archivo `.env` con:

```env
# Supabase Configuration
SUPABASE_URL=https://ajqkrulblcfjvbfobiph.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# Database Configuration
DATABASE_URL=postgresql://postgres:password@db.ajqkrulblcfjvbfobiph.supabase.co:5432/postgres

# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=eWash API
DEBUG=True

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

5. **Ejecutar la aplicación**

```bash
python run.py
```

O usando uvicorn directamente:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

1. **Login**: `POST /api/v1/auth/login`
2. **Usar token**: Incluir en headers: `Authorization: Bearer <token>`

## 🏢 Arquitectura Multi-Tenant

El sistema soporta múltiples organizaciones:

- **Organización Principal**: Administradora central
- **Sucursales**: Sublocales dependientes
- **Aislamiento de datos**: Cada organización solo ve sus datos

## 📊 Modelos de Datos

### Entidades Principales

- **Organization**: Organizaciones (administradora/sucursales)
- **User**: Usuarios del sistema con roles
- **Client**: Clientes de la organización
- **Vehicle**: Vehículos de los clientes
- **Employee**: Empleados de la organización
- **Service**: Servicios ofrecidos
- **Order**: Órdenes de servicio

### Relaciones

- Una organización puede tener múltiples usuarios, clientes, empleados y servicios
- Un cliente puede tener múltiples vehículos
- Una orden conecta cliente, vehículo, servicio y empleado

## 🔧 Endpoints Principales

### Autenticación

- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/test-token` - Verificar token

### Usuarios

- `GET /api/v1/users/` - Listar usuarios
- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/me` - Usuario actual
- `PUT /api/v1/users/me` - Actualizar perfil

### Organizaciones

- `GET /api/v1/organizations/me` - Mi organización
- `PUT /api/v1/organizations/me` - Actualizar organización

### Clientes

- `GET /api/v1/clients/` - Listar clientes
- `POST /api/v1/clients/` - Crear cliente
- `GET /api/v1/clients/search?q=query` - Buscar clientes
- `GET /api/v1/clients/{id}` - Obtener cliente
- `PUT /api/v1/clients/{id}` - Actualizar cliente

### Servicios

- `GET /api/v1/services/` - Listar servicios
- `POST /api/v1/services/` - Crear servicio
- `GET /api/v1/services/{id}` - Obtener servicio

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app tests/
```

## 🔒 Seguridad

- **Autenticación JWT** con expiración configurable
- **Validación de datos** con Pydantic
- **Aislamiento multi-tenant** por organización
- **Hashing de contraseñas** con bcrypt
- **CORS** configurado para frontend

## 📈 Monitoreo

- **Health check**: `GET /health`
- **Logs estructurados** con uvicorn
- **Métricas de base de datos** incluidas

## 🚀 Despliegue

### Desarrollo

```bash
python run.py
```

### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker (opcional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**eWash Backend** - API robusta para gestión de lavaderos de autos 🚗✨

Credenciales:
📧 Email: admin@ewash.com
🔑 Contraseña: admin123
👑 Rol: super_admin
🏢 Organización: eWash Administración

uvicorn app.main:app --reload

pip install -r requirements.txt

```plaintext
http://127.0.0.1:8000
```

## Rutas de la API

La API estará disponible en las siguientes rutas:

- **Página principal**: `http://127.0.0.1:8000/`
- **Documentación Swagger**: `http://127.0.0.1:8000/docs`
- **Documentación ReDoc**: `http://127.0.0.1:8000/redoc`
- **Endpoints de la API**: `http://127.0.0.1:8000/api/v1/...`

### Endpoints principales:

1. **Autenticación**:

1. Login: `POST http://127.0.0.1:8000/api/v1/auth/login/access-token`

1. **Administradores**:

1. Listar: `GET http://127.0.0.1:8000/api/v1/administradores/`
1. Crear: `POST http://127.0.0.1:8000/api/v1/administradores/`
1. Obtener: `GET http://127.0.0.1:8000/api/v1/administradores/{id}`
1. Actualizar: `PUT http://127.0.0.1:8000/api/v1/administradores/{id}`
1. Eliminar: `DELETE http://127.0.0.1:8000/api/v1/administradores/{id}`

1. **Sedes**:

1. Listar: `GET http://127.0.0.1:8000/api/v1/sedes/`
1. Crear: `POST http://127.0.0.1:8000/api/v1/sedes/`
1. Obtener: `GET http://127.0.0.1:8000/api/v1/sedes/{id}`
1. Actualizar: `PUT http://127.0.0.1:8000/api/v1/sedes/{id}`
1. Eliminar: `DELETE http://127.0.0.1:8000/api/v1/sedes/{id}`

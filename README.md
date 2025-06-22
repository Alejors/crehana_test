# TASKS MANAGER 

Este proyecto es un servicio backend que permite la gestión de listas de tareas y las tareas asociadas a cada lista. Entre sus funcionalidades principales están:

- Crear, editar, listar y eliminar listas de tareas.

- Crear, editar, listar y eliminar tareas dentro de listas específicas.

- Calcular y entregar el porcentaje de completitud de cada lista basado en las tareas que contiene.

- Filtrar tareas mediante parámetros en la URL (query params), por ejemplo:

    - `priority__in=high,medium` para filtrar tareas con prioridad alta o media.
    - `is_completed=true` para filtrar tareas completadas.
    - Filtros por fechas como `created_at__gte=2025-06-20` para tareas creadas a partir de una fecha.

- Implementa autenticación con registro y login de usuarios.

- Protege rutas sensibles usando JWT almacenados en cookies para asegurar acceso autenticado.

## 🛠️ Instalación y configuración

### Requisitos

- Docker
- Docker Compose

### Instalación y despliegue

1. Clona el repositorio:

```bash
git clone git@github.com:Alejors/crehana_test.git
cd crehana_test
```

2. Crea un archivo `.env` tomando como referencia las variables presentes en `.env.example`.

```bash
cp .env.example .env
```

3. Levanta los servicios:

```bash
docker-compose up --build
```

Esto levantará:

- Backend Python
- Base de datos

> El backend estará accesible en `http://localhost:8000` tomando los valores propuestos en el ejemplo.

#### Opcional: Seeder

Se agregó un archivo `.sql` dentro de `/infrastructure/db/seed`. Este se encarga de cargar datos iniciales para poder probar endpoints.

Para utilizar se puede correr el siguiente comando:

```bash
docker-compose exec -T db mysql -uroot -proot tasks_manager < ./app/infrastructure/db/seed/seeder.sql
```

> Este comando crea usuarios de prueba con la clave `random1234`.

## 🧪 Ejemplo de uso

1. **Iniciar sesión** (con esto se setea la cookie que permite el acceso a las rutas protegidas).

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user1@example.com",
  "password": "yourpassword"
}
```

> Esto almacenará una cookie `access_token` automáticamente en el navegador o cliente HTTP.

2. **Crear una lista de tareas:**

```http
POST /api/v1/task-lists
Content-Type: application/json

{
  "name": "Mi nueva lista"
}
```

3. **Crear una tarea en esa lista:**

```http
POST /api/v1/task-lists/1/tasks
Content-Type: application/json

{
  "description": "Comprar pan",
  "is_completed": false,
  "priority": "low",
  "assigned_user_email": "user2@example.com"
}
```

> El campo `assigned_user_email` es opcional. Si se proporciona y el usuario no existe, se simula una invitación por correo.

4. **Listar tareas con filtros** (por ejemplo, tareas incompletas con prioridad baja o media, creadas después del 2025-06-20):

```http
GET /api/v1/task-lists/1/tasks?is_completed=false&priority__in=low,medium&created_at__gte=2025-06-20
```

5. **Actualizar el estado de tareas:**

```http
PUT /api/v1/tasks/1
Content-Type: application/json

{
  "is_completed": true
}
```

> También se puede modificar la descripción (`description`) o prioridad (`priority`) de una tarea, pero **NO** la lista a la que pertenece.

*Nota*: las prioridades están establecidas por un ENUM de base de datos, por lo cual sólo se puede definir 3 prioridades: `low`, `medium` o `high`.

## 📚 Mapa de la API

### Endpoints principales

- `POST /api/v1/register` - Registro de usuario.

- `POST /api/v1/login` - Login de usuario, devuelve JWT en cookie.

- `POST /api/v1/logout`- Quitar Cookie JWT, bloquea acceso a rutas protegidas.

- `GET /api/v1/task-lists` - Listar todas las listas de tareas.

- `POST /api/v1/task-lists` - Crear una nueva lista de tareas.

- `GET /api/v1/task-lists/{task_list_id}` - Obtener una lista específica.

- `PUT /api/v1/task-lists/{task_list_id}` - Actualizar una lista de tareas.

- `DELETE /api/v1/task-lists/{task_list_id}` - Eliminar una lista de tareas (requiere que no tenga tareas incompletas).

- `GET /api/v1/task-lists/{task_list_id}/tasks` - Obtener tareas de una lista, admite filtros en query params.

- `POST /api/v1/task-lists/{task_list_id}/tasks` - Crear tarea en una lista.

- `PUT /api/v1/tasks/{task_id}` - Actualizar tarea.

- `DELETE /api/v1/tasks/{task_id}` - Eliminar tarea.

## 🔐 Seguridad

- Autenticación mediante JWT guardados en cookies HttpOnly.

- Middleware que protege rutas para usuarios autenticados únicamente.

- Validaciones en backend para impedir operaciones inválidas (ejemplo: eliminar listas con tareas incompletas).

## 🔧 Tecnologías y librerías principales
- Python 3.11

- FastAPI

- SQLAlchemy

- MySQL como base de datos relacional

- PyJWT para manejo de tokens JWT

- Passlib con bcrypt para manejo seguro de contraseñas

- Docker + Docker Compose para contenerización y orquestación

## 🧪 Testing

- Pruebas unitarias y de integración con Pytest y TestClient de FastAPI.

- Mocking con AsyncMock para aislamiento en pruebas.

- Cobertura para casos de rutas, validaciones y lógica de negocio.

### Ejecutar Pruebas

Después de haber tener levantado tanto el servicio como la base de datos según las [instrucciones](#instalación-y-despliegue) se debe ejecutar el comando desde una terminal:

```bash
docker-compose exec api python -m pytest
```

Esto se encarga de correr todos los tests del directorio `/tests`.

## 🧹 Estilo de código

Este proyecto utiliza [Black](https://black.readthedocs.io/en/stable/) como formateador de código y [Flake8](https://flake8.pycqa.org/en/latest/) como linter para asegurar una base de código limpia y consistente.

### Uso de herramientas

- **Formatear el código con Black:**

```bash
dc exec api black .
```

- **Verificar problemas con Flask8**

```bash
dc exec api flake8 .
```

> Se recomienda configurar el editor para ejecutar automáticamente Black y Flake8 al guardar.

## Reglas Flake8 relevantes

- `E203`y `W503` están ignoradas por compatibilidad con Black. Esto viene definido en el archivo `.flake8`.

```ini
[flake8]
ignore = E203, W503
```
# TASKS MANAGER 

Este proyecto crea listas de tareas y las tareas asociadas a una lista. Permite buscar tareas según lista, porcentaje de compleción y otras características.

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

> El backend estará accesible en `http://localhost:{VALOR_DE:DOCKER_SERVICE_PORT}`

# 2025-06-20 

## -- Inicialización del proyecto y estructura base

- **Decisión**: Crear una estructura base con separación de capas (domain, infrastructure, usecases, api).

- **Motivación**: Permitir escalabilidad, fácil mantenimiento, claridad en responsabilidades y mantener limpieza del código.

- **Consideración**: Se sigue una arquitectura inspirada en principio de Clean Architecture.

## -- Declarative Base y creación automática de tablas

- **Decisión**: Usar SQLAlchemy con declarative_base() y autogeneración de tablas al levantar la app.

- **Motivación**: Agilizar el desarrollo inicial al tratarse de una prueba técnica. 

- **Consideración**: En un entorno productivo, esta estrategia sería reemplazada por un sistema de migraciones como `Alembic`.

## -- Modelado inicial de `TaskList` y `Task`

- **Decisión**: Crear modelos con SQLAlchemy extendiendo un `TimestampMixin`.

- **Motivación**: Reutilizar las columnas `created_at`, `updated_at`, y `deleted_at` sin repetir código.

- **Consideración**: Este enfoque va de la mano de generar actualizaciones automáticas a la columna `updated_at` y utilizar la columna `deleted_at` como indicador de *soft-delete*.

## -- Entidades y DTOs con Pydantic

- **Decisión**: Separar modelos Pydantic (DTOs) de los modelos SQLAlchemy. Asimismo no relacionar directamente un ORM con los datos de salida, respetando que la lógica de negocio se ejecute sobre entidades de dominio.

- **Motivación**: Aislar la lógica de validación de datos y la estructura de serialización de la capa ORM.

## -- Repositorios basados en interfaces

- **Decisión**: Definir interfaces de repositorios que los casos de uso consumirán.

- **Motivación**: Promover el desacoplamiento y facilitar testeo o reemplazo de implementación. Permite eventualmente cambiar de un ORM a otro si se deseara. Respetar principio **SOLID**.

## -- Inyección de dependencias en rutas

- **Decisión**: Las rutas reciben los casos de uso como dependencias.

- **Motivación**: Cumplir con el principio de inversión de dependencias y mantener la lógica fuera de los controladores.

# 2025-06-21

## -- Sistema de filtros dinámicos

- **Decisión**: Crear un utilitario para convertir diccionarios de query params en filtros SQLAlchemy compatibles.

- **Motivación**: Evitar lógica duplicada en diferentes repositorios al implementar filtros flexibles y reutilizables.

- **Consideración**: El utilitario es propio del ORM, siendo que las rutas y `query_params` deberían ser fijos. En caso que se modifique el ORM, se puede usar como base para definir los operadores necesarios para mantener el comportamiento.

## -- Soporte para autenticación con JWT cookies

- **Decisión**: Implementar autenticación mediante login y registro usando JWT en cookies HTTPOnly.

- **Motivación**: Asegurar rutas protegidas sin exponer el token al frontend. No se puede obtener el token mediante *scripts* y herramientas como Postman también reciben y setean el Cookie satisfactoriamente.

- **Consideración**: Se usó `pyjwt` para mantener la simplicidad. En caso de necesitar una librería más robusta, se podría optar por `python-jose`.

## -- Utilizar Interfaz para Servicio de Mailing

- **Decisión**: Igual que para repositorios de persistencia de información, se decide crear una interfaz para el servicio de correo.

- **Motivación**: Si bien se solicita un servicio "ficticio", al crear una interfaz y respetar la inyección de dependencias, se podría crear un servicio concreto real que respete la interfaz y mantener la lógica intacta.

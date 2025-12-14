
# Proyecto API de Productos (Django REST Framework)

Este documento proporciona una guía detallada sobre la arquitectura, configuración y uso de la API de Productos. El proyecto está construido con Django y Django REST Framework, y ofrece un conjunto completo de endpoints para la gestión de un inventario de productos.

##  Índice

1.  [Descripción General](#descripción-general)
2.  [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3.  [Tecnologías y Librerías](#tecnologías-y-librerías)
4.  [Guía de Instalación y Despliegue](#guía-de-instalación-y-despliegue)
5.  [Análisis Detallado de Archivos](#análisis-detallado-de-archivos)
    *   [settings.py](#proyectosettingspy)
    *   [urls.py (Proyecto)](#proyectosenaurlspy)
    *   [models.py](#appsproductosmodelspy)
    *   [serializers.py](#appsproductosserializerspy)
    *   [views.py](#appsproductosviewspy)
    *   [urls.py (Aplicación)](#appsproductosurlspy)
6.  [Endpoints de la API](#endpoints-de-la-api)
7.  [Buenas Prácticas y Puntos de Mejora](#buenas-prácticas-y-puntos-de-mejora)

## Descripción General

La API de Productos es un servicio backend que permite realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre una base de datos de productos. Ha sido diseñada siguiendo los principios REST y utilizando las herramientas proporcionadas por Django REST Framework para un desarrollo rápido y eficiente.

El flujo de una petición típica es:
1.  Un cliente HTTP (como una aplicación frontend en React, Vue, etc.) realiza una petición a un endpoint, por ejemplo, `GET /api/productos/`.
2.  El enrutador principal de Django (`proyectoSena/urls.py`) delega la petición a la aplicación de `Productos`.
3.  El enrutador de la aplicación (`apps/Productos/urls.py`) asocia la ruta con la vista `ProductoView`.
4.  La vista (`ProductoView`) procesa la petición, interactúa con el modelo `Producto` para consultar la base de datos y utiliza `ProductoSerializer` para convertir los datos al formato JSON.
5.  La respuesta JSON es enviada de vuelta al cliente.

## Arquitectura del Proyecto

El proyecto sigue la arquitectura estándar de Django, que promueve la separación de responsabilidades:

-   **`proyectoSena/`**: Es el directorio del proyecto principal. Contiene la configuración global (`settings.py`) y el enrutador de URLs principal (`urls.py`).
-   **`apps/Productos/`**: Es una aplicación de Django autocontenida que encapsula toda la lógica relacionada con los productos (modelos, vistas, serializadores y URLs específicas). Esta modularidad facilita el mantenimiento y la reutilización.
-   **`manage.py`**: El script de utilidad de Django para ejecutar comandos administrativos.
-   **`Pipfile`**: Define las dependencias del proyecto, gestionadas a través de `pipenv`.

## Tecnologías y Librerías

Las dependencias principales del proyecto se definen en el archivo `Pipfile`:

```toml
[packages]
django = "*"
djangorestframework = "*"
django-cors-headers = "*"
```

-   **Django**: El framework web principal sobre el que se construye todo.
-   **Django REST Framework (DRF)**: La librería clave para construir APIs RESTful de forma rápida y robusta.
-   **django-cors-headers**: Un middleware para gestionar las políticas de Cross-Origin Resource Sharing (CORS), permitiendo que un frontend alojado en un dominio diferente pueda comunicarse con esta API.

## Guía de Instalación y Despliegue

Para replicar este proyecto en un entorno de desarrollo local, sigue estos pasos:

1.  **Prerrequisitos**:
    *   Tener Python 3.10 o superior instalado.
    *   Tener `pipenv` instalado (`pip install pipenv`).

2.  **Clonar el Repositorio**:
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

3.  **Crear el Entorno Virtual e Instalar Dependencias**:
    `pipenv` leerá el `Pipfile` y creará un entorno virtual con todas las librerías necesarias.
    ```bash
    pipenv install
    ```

4.  **Activar el Entorno Virtual**:
    ```bash
    pipenv shell
    ```

5.  **Aplicar las Migraciones**:
    Este comando creará la base de datos `db.sqlite3` y las tablas necesarias según los modelos definidos.
    ```bash
    python manage.py migrate
    ```

6.  **Ejecutar el Servidor de Desarrollo**:
    ```bash
    python manage.py runserver
    ```
    La API estará disponible en `http://127.0.0.1:8000/api/productos/`.

## Análisis Detallado de Archivos

### `proyectoSena/settings.py`

Es el corazón de la configuración del proyecto. Los puntos más relevantes son:

-   **`SECRET_KEY`**: Una clave única para la seguridad de la instancia. **No debe ser expuesta en producción.**
-   **`DEBUG`**: Activado (`True`) para desarrollo. Muestra páginas de error detalladas. **Debe ser `False` en producción.**
-   **`INSTALLED_APPS`**: Aquí se registran todas las aplicaciones que Django debe cargar. Es crucial haber añadido `'rest_framework'`, `'corsheaders'` y la aplicación local `'apps.Productos'`.
-   **`MIDDLEWARE`**: Se añade `'corsheaders.middleware.CorsMiddleware'` para procesar las cabeceras CORS en las peticiones.
-   **`DATABASES`**: Configurado por defecto para usar `SQLite`, una base de datos ligera y basada en archivos, ideal para desarrollo.
-   **`CORS_ALLOWED_ORIGINS`**: Una lista de orígenes (dominios) que tienen permitido hacer peticiones a esta API. En este caso, se permite el acceso desde un servidor de desarrollo frontend en `localhost:5173`.

### `proyectoSena/urls.py`

El enrutador principal del proyecto. Su función es delegar las rutas a las aplicaciones correspondientes.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("apps.Productos.urls"))
]
```

-   Cualquier petición que comience con `/api/` es redirigida al archivo `urls.py` de la aplicación `Productos`. Esto mantiene el enrutamiento limpio y modular.

### `apps/Productos/models.py`

Define la estructura de la tabla de productos en la base de datos.

```python
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(blank=False, null=False)
    
    def __str__(self):
        return f"{self.nombre}"
```

-   **`Producto`**: Un modelo de Django que se traduce en una tabla en la base de datos.
-   **Campos**:
    -   `nombre`: Un campo de texto con un máximo de 250 caracteres.
    -   `precio`: Un campo decimal, ideal para valores monetarios para evitar errores de precisión.
    -   `stock`: Un campo de número entero.

### `apps/Productos/serializers.py`

Actúa como un traductor entre los objetos del modelo `Producto` y el formato JSON que la API consume y produce.

```python
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']
        read_only_fields = ['id']
```

-   `ModelSerializer`: Una clase de DRF que automáticamente genera los campos del serializador a partir de un modelo.
-   `Meta.model`: Especifica que este serializador está vinculado al modelo `Producto`.
-   `Meta.fields`: Define los campos del modelo que serán incluidos en la representación JSON.
-   `Meta.read_only_fields`: El campo `id` es de solo lectura, ya que es generado automáticamente por la base de datos.

### `apps/Productos/views.py`

Contiene la lógica de negocio de la API.

```python
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

-   **`ModelViewSet`**: Una clase de DRF extremadamente potente que proporciona por defecto la funcionalidad completa para las operaciones CRUD (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`).
-   `queryset`: Define el conjunto de objetos sobre los que operará esta vista (todos los productos).
-   `serializer_class`: Especifica el serializador que se debe usar para convertir los datos.

### `apps/Productos/urls.py`

Define los endpoints específicos de la API de Productos.

```python
from rest_framework.routers import SimpleRouter
from .views import ProductoView

router = SimpleRouter(trailing_slash=True)
router.register("productos", ProductoView)

urlpatterns = router.urls
```

-   `SimpleRouter`: Una clase de DRF que registra un `ViewSet` y genera automáticamente las rutas URL para todas las acciones CRUD siguiendo las convenciones REST.

## Endpoints de la API

Gracias al uso de `ModelViewSet` y `SimpleRouter`, la API expone los siguientes endpoints de forma automática:

| Endpoint                  | Método HTTP | Acción                         | Descripción                                |
| ------------------------- | ----------- | ------------------------------ | ------------------------------------------ |
| `/api/productos/`         | `GET`       | `list`                         | Obtiene una lista de todos los productos.  |
| `/api/productos/`         | `POST`      | `create`                       | Crea un nuevo producto.                    |
| `/api/productos/<int:pk>/` | `GET`       | `retrieve`                     | Obtiene un producto específico por su ID.  |
| `/api/productos/<int:pk>/` | `PUT`       | `update`                       | Actualiza un producto completo por su ID.  |
| `/api/productos/<int:pk>/` | `PATCH`     | `partial_update`               | Actualiza parcialmente un producto por su ID.|
| `/api/productos/<int:pk>/` | `DELETE`    | `destroy`                      | Elimina un producto por su ID.             |

## Buenas Prácticas y Puntos de Mejora

### Buenas Prácticas Implementadas

-   **Separación de Responsabilidades**: El proyecto está bien organizado en una aplicación (`Productos`) dedicada.
-   **Código DRY (Don't Repeat Yourself)**: El uso de `ModelViewSet` y `ModelSerializer` reduce drásticamente el código repetitivo.
-   **Modularidad de URLs**: El enrutamiento está desacoplado entre el proyecto principal y la aplicación.
-   **Modelo de Datos Correcto**: Se utiliza `DecimalField` para el precio, lo que previene errores de punto flotante.

### Puntos de Mejora Sugeridos

-   **Fijar Versiones de Dependencias**: En `Pipfile`, las dependencias están como `"*"`. Para un entorno de producción estable, es crucial fijar versiones específicas (ej. `django = "4.2.5"`) para evitar que actualizaciones automáticas rompan el proyecto.
-   **Seguridad en Producción**:
    -   La `SECRET_KEY` no debe estar hardcodeada. Debe cargarse desde una variable de entorno.
    -   El modo `DEBUG` debe estar desactivado (`DEBUG = False`).
-   **Autenticación y Autorización**: Actualmente, la API es pública. Para un caso de uso real, se deberían implementar clases de autenticación y permisos en la `ProductoView` para restringir quién puede realizar ciertas acciones. Ejemplo:
    ```python
    from rest_framework.permissions import IsAuthenticated
    
    class ProductoView(viewsets.ModelViewSet):
        # ...
        permission_classes = [IsAuthenticated] 
    ```
-   **Base de Datos de Producción**: SQLite no es recomendable para producción. Se debería configurar una base de datos más robusta como PostgreSQL o MySQL.

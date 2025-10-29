# Sistema de Gestión de Vuelos - Aerolínea

## 📋 Descripción del Proyecto

Sistema completo de gestión de vuelos desarrollado con Django y Django Rest Framework. Incluye funcionalidades para gestionar vuelos, pasajeros, reservas, aviones y boletos, con una API REST completa y documentación interactiva.

## 🚀 Características Principales

### Funcionalidades Web
- ✅ Gestión de vuelos, pasajeros y reservas
- ✅ Interfaz web responsive
- ✅ Autenticación de usuarios
- ✅ Internacionalización (español/inglés)

### API REST
- ✅ Endpoints completos para todas las entidades
- ✅ Autenticación JWT
- ✅ Permisos y roles (admin/usuario)
- ✅ Filtros y búsquedas avanzadas
- ✅ Documentación Swagger interactiva

### Testing
- ✅ Tests unitarios completos
- ✅ Cobertura de endpoints API
- ✅ Tests de autenticación y permisos

## 🛠️ Tecnologías Utilizadas

- **Django 5.2.3** - Framework web
- **Django Rest Framework** - API REST
- **JWT Authentication** - Autenticación
- **Swagger/OpenAPI** - Documentación
- **SQLite** - Base de datos
- **Bootstrap** - Frontend

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone [url-del-repositorio]
cd EFI-ing-Aerolinea/aerolinea
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor
```bash
python manage.py runserver
```

## 🧪 Ejecución de Tests

El proyecto incluye tests con el runner de Django (unittest) y es compatible con pytest (si prefieres usarlo). A continuación tienes instrucciones claras para ambos enfoques.

Recomendación: usa el runner de Django para ejecutar rápidamente (`manage.py test`) o `pytest` si quieres fixtures y salida adicional.

### Usando el runner de Django (por defecto)

Ejecuta los tests desde la carpeta del proyecto (donde está `manage.py`):

```zsh
cd /ruta/al/proyecto/aerolinea
source .venv/bin/activate    # si usas un virtualenv
python manage.py test
```

Algunos comandos útiles:

- Ejecutar todos los tests:
  ```zsh
  python manage.py test
  ```
- Ejecutar un archivo/módulo concreto (ej.: tests del API):
  ```zsh
  python manage.py test api.tests
  ```
- Ejecutar una clase concreta:
  ```zsh
  python manage.py test api.tests.test_flights_api.TestFlightsAPI
  ```
- Ejecutar un método concreto:
  ```zsh
  python manage.py test api.tests.test_flights_api.TestFlightsAPI.test_list_flights
  ```
- Ejecutar con más verbosidad:
  ```zsh
  python manage.py test -v 2
  ```

### Usando pytest (opcional)

Si prefieres pytest, ya se agregó un `pytest.ini` que configura `DJANGO_SETTINGS_MODULE`. Instala `pytest` y `pytest-django`:

```zsh
source .venv/bin/activate
pip install pytest pytest-django
pytest -q
```

- Ejecutar un archivo concreto con pytest:
  ```zsh
  pytest api/tests/test_flights_api.py -q
  ```
- Ejecutar una prueba concreta:
  ```zsh
  pytest api/tests/test_flights_api.py::TestFlightsAPI::test_list_flights -q
  ```


- Asegúrate de ejecutar los tests desde la raíz del proyecto (donde está `manage.py`).
- Si pytest no encuentra Django settings, confirma que `pytest.ini` contiene `DJANGO_SETTINGS_MODULE = aerolinea.settings`.
- Para tests que usan la base de datos, `pytest-django` gestionará la creación/rollback de la DB de pruebas.

### Resultado esperado

Cuando todo pase verás algo como:

```
Found 17 test(s).
----------------------------------------------------------------------
Ran 17 tests in 11.9s
OK
```

Si hay fallos, copia la salida y la revisamos juntos.


## 🌐 Uso de la API

### 1. Acceder a la documentación
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **API Endpoints**: `http://127.0.0.1:8000/api/`

### Swagger (drf-yasg)

La documentación interactiva Swagger ya está configurada en el proyecto y expuesta en `/swagger/`.

- Iniciar servidor:
  ```zsh
  python manage.py runserver
  # luego abrir en el navegador http://127.0.0.1:8000/swagger/
  ```

- Probar endpoints protegidos (JWT):
  1. Obtener tokens:
     ```zsh
     curl -X POST http://127.0.0.1:8000/api/token/ \
       -H "Content-Type: application/json" \
       -d '{"username": "tu_usuario", "password": "tu_password"}'
     ```
  2. En Swagger UI pulsa "Authorize" e ingresa en el campo:
     ```text
     Bearer <tu_token_jwt>
     ```
     Esto añadirá el header `Authorization` a las peticiones desde la UI.

- Configuración recomendada (opcional):
  En `settings.py` puedes añadir entrada para que Swagger UI reconozca la definición de seguridad:

  ```py
  SWAGGER_SETTINGS = {
      'SECURITY_DEFINITIONS': {
          'Bearer': {
              'type': 'apiKey',
              'name': 'Authorization',
              'in': 'header',
              'description': "JWT Authorization header. Ejemplo: 'Authorization: Bearer <token>'",
          }
      },
  }
  ```

- Poner Swagger en español (opcional):
  - Los textos de `openapi.Info` (título, descripción) ya están en español en `urls.py`.
  - Para traducir la interfaz (botones, labels) puedes sobreescribir la plantilla de drf-yasg `swagger-ui.html` en `templates/drf_yasg/swagger-ui.html` y forzar `lang: 'es'` al inicializar `SwaggerUIBundle`, o incluir un pequeño script que reemplace los textos visibles.
  - Si quieres, puedo crear el template override y un script de traducción rápida.


### 2. Autenticación JWT
```bash
# Obtener token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'

# Usar token en peticiones
curl -H "Authorization: Bearer tu_token_aqui" \
  http://127.0.0.1:8000/api/flights/
```

### 3. Endpoints Principales

#### Vuelos
- `GET /api/flights/` - Listar vuelos
- `POST /api/flights/` - Crear vuelo (admin)
- `GET /api/flights/search/` - Buscar vuelos

#### Pasajeros
- `GET /api/passengers/` - Listar pasajeros
- `POST /api/passengers/` - Crear pasajero (admin)

#### Reservas
- `GET /api/reservations/` - Listar reservas
- `POST /api/reservations/` - Crear reserva
- `POST /api/reservations/{id}/confirm/` - Confirmar reserva

## 📁 Estructura del Proyecto

```
aerolinea/
├── gestionVuelos/
│   ├── models.py          # Modelos de datos
│   ├── views_api.py       # API REST endpoints
│   ├── serializers.py     # Serializers para API
│   ├── tests_api.py       # Tests unitarios
│   ├── urls_api.py        # URLs de la API
│   └── templates/         # Templates web
├── aerolinea/
│   ├── settings.py        # Configuración Django
│   └── urls.py           # URLs principales
└── requirements.txt      # Dependencias
```

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Ejecutar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Testing
```bash
# Ejecutar todos los tests
python manage.py test

# Tests con verbosidad
python manage.py test -v 2

# Tests específicos
python manage.py test gestionVuelos.tests_api
```

### Base de Datos
```bash
# Resetear base de datos
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 📚 Documentación Adicional

- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **JWT Authentication**: https://django-rest-framework-simplejwt.readthedocs.io/
- **Swagger**: https://drf-yasg.readthedocs.io/

## 👨‍💻 Desarrollado por

**Estudiante de Ingeniería**  
**Fecha**: 2024  
**Proyecto**: Sistema de Gestión de Vuelos

---

## 🎯 Resumen de Tests

- **Total de tests**: 13
- **Cobertura**: Endpoints API completos
- **Autenticación**: JWT implementada
- **Permisos**: Admin vs Usuario normal
- **Estado**: ✅ Todos los tests pasando

¡El proyecto está listo para usar y entregar! 🚀

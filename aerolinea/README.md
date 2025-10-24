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

### Tests Unitarios de la API

El proyecto incluye tests unitarios completos para todos los endpoints de la API. Aquí te explico cómo ejecutarlos:

#### 1. Ejecutar todos los tests de la API
```bash
python manage.py test gestionVuelos.tests_api
```

#### 2. Ejecutar tests específicos por clase
```bash
# Tests de vuelos
python manage.py test gestionVuelos.tests_api.FlightAPITestCase

# Tests de pasajeros
python manage.py test gestionVuelos.tests_api.PassengerAPITestCase

# Tests de reservas
python manage.py test gestionVuelos.tests_api.ReservationAPITestCase

# Tests de boletos
python manage.py test gestionVuelos.tests_api.TicketAPITestCase
```

#### 3. Ejecutar un test específico
```bash
# Ejemplo: test de listar vuelos
python manage.py test gestionVuelos.tests_api.FlightAPITestCase.test_list_flights_authorized
```

#### 4. Ejecutar con verbosidad
```bash
# Mostrar detalles de cada test
python manage.py test gestionVuelos.tests_api -v 2

# Mostrar solo los nombres de los tests
python manage.py test gestionVuelos.tests_api -v 1
```

#### 5. Ejecutar tests con cobertura
```bash
# Instalar coverage (opcional)
pip install coverage

# Ejecutar con cobertura
coverage run --source='.' manage.py test gestionVuelos.tests_api
coverage report
coverage html  # Genera reporte HTML
```

### Cobertura de Tests

Los tests cubren:

#### **FlightAPITestCase** (5 tests)
- ✅ Listar vuelos sin autenticación
- ✅ Listar vuelos con autenticación  
- ✅ Crear vuelos (solo administradores)
- ✅ Buscar vuelos por origen/destino
- ✅ Ver pasajeros de vuelo (solo administradores)

#### **PassengerAPITestCase** (2 tests)
- ✅ Crear pasajeros (solo administradores)
- ✅ Ver reservas de pasajero

#### **ReservationAPITestCase** (4 tests)
- ✅ Crear reserva
- ✅ Verificar disponibilidad de asiento
- ✅ Confirmar reserva
- ✅ Cancelar reserva

#### **TicketAPITestCase** (2 tests)
- ✅ Generar boleto (solo administradores)
- ✅ Consultar boleto por código

### Interpretación de Resultados

#### ✅ Tests Exitosos
```
.............  # 13 tests ejecutados
----------------------------------------------------------------------
Ran 13 tests in 18.977s
OK
```

#### ❌ Tests Fallidos
```
F............  # 1 test falló
----------------------------------------------------------------------
FAIL: test_create_flight_admin_only
```

## 🌐 Uso de la API

### 1. Acceder a la documentación
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **API Endpoints**: `http://127.0.0.1:8000/api/`

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

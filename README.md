# 🛩️ Sistema de Gestión de Aerolínea

Sistema completo de gestión de aerolínea desarrollado con Django y Django Rest Framework, que incluye funcionalidades web tradicionales y API REST para integración con aplicaciones móviles y sistemas externos.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso Web](#-uso-web)
- [API REST](#-api-rest)
- [Tests Unitarios](#-tests-unitarios)
- [Documentación](#-documentación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Autenticación](#-autenticación)
- [Contribución](#-contribución)

## ✨ Características

### 🌐 Interfaz Web
- **Gestión de Vuelos**: Crear, editar, listar y buscar vuelos
- **Gestión de Pasajeros**: Registro y administración de pasajeros
- **Sistema de Reservas**: Reservar asientos y gestionar reservas
- **Gestión de Aviones**: Administrar flota de aviones
- **Interfaz Responsive**: Diseño adaptable a diferentes dispositivos

### 🔌 API REST
- **Endpoints Completos**: CRUD para todas las entidades
- **Autenticación JWT**: Sistema seguro de autenticación
- **Permisos y Roles**: Administradores vs usuarios normales
- **Filtros Avanzados**: Búsqueda y filtrado de datos
- **Documentación Interactiva**: Swagger UI integrado

### 🧪 Testing
- **Tests Unitarios**: Cobertura completa de endpoints API
- **Tests de Autenticación**: Validación de permisos y roles
- **Tests de Funcionalidad**: Verificación de operaciones CRUD

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.2.3** - Framework web principal
- **Django Rest Framework** - API REST
- **JWT Authentication** - Autenticación segura
- **SQLite** - Base de datos (desarrollo)
- **Django Filters** - Filtrado avanzado
- **DRF-YASG** - Documentación automática

### Frontend
- **HTML5/CSS3** - Interfaz web
- **Bootstrap** - Framework CSS
- **JavaScript** - Interactividad

### Herramientas
- **Sentry** - Monitoreo de errores
- **Git** - Control de versiones

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

### 1. Clonar el repositorio
```bash
git clone [url-del-repositorio]
cd EFI-ing-Aerolinea/aerolinea
```

### 2. Crear entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
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
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
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

## ⚙️ Configuración

### Variables de Entorno
El proyecto está configurado para desarrollo. Para producción, configura:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECRET_KEY = 'tu-secret-key-seguro'
```

### Base de Datos
Por defecto usa SQLite. Para producción, configura PostgreSQL o MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aerolinea_db',
        'USER': 'usuario',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🌐 Uso Web

### Acceso al Sistema
1. Navega a `http://127.0.0.1:8000/`
2. Inicia sesión con tu usuario
3. Explora las diferentes secciones:
   - **Vuelos**: Gestionar vuelos disponibles
   - **Pasajeros**: Administrar pasajeros
   - **Reservas**: Crear y gestionar reservas
   - **Aviones**: Gestionar flota

### Funcionalidades Web
- **Dashboard**: Vista general del sistema
- **Gestión de Vuelos**: CRUD completo de vuelos
- **Gestión de Pasajeros**: Registro y administración
- **Sistema de Reservas**: Reservar asientos
- **Reportes**: Consultas y estadísticas

## 🔌 API REST

### Acceso a la Documentación
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **API Base**: `http://127.0.0.1:8000/api/`

### Autenticación JWT

#### 1. Obtener Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
```

#### 2. Usar Token en Peticiones
```bash
curl -H "Authorization: Bearer tu_token_aqui" \
  http://127.0.0.1:8000/api/flights/
```

### Endpoints Principales

#### Vuelos
- `GET /api/flights/` - Listar vuelos
- `POST /api/flights/` - Crear vuelo (admin)
- `GET /api/flights/{id}/` - Detalle de vuelo
- `GET /api/flights/search/` - Buscar vuelos
- `GET /api/flights/{id}/passengers/` - Pasajeros por vuelo (admin)

#### Pasajeros
- `GET /api/passengers/` - Listar pasajeros
- `POST /api/passengers/` - Crear pasajero (admin)
- `GET /api/passengers/{id}/reservations/` - Reservas del pasajero

#### Reservas
- `GET /api/reservations/` - Listar reservas
- `POST /api/reservations/` - Crear reserva
- `GET /api/reservations/check_seat/` - Verificar asiento
- `POST /api/reservations/{id}/confirm/` - Confirmar reserva
- `POST /api/reservations/{id}/cancel/` - Cancelar reserva

#### Aviones
- `GET /api/planes/` - Listar aviones
- `GET /api/planes/{id}/seats/` - Asientos del avión

#### Boletos
- `GET /api/tickets/` - Listar boletos
- `GET /api/tickets/by_barcode/` - Consultar por código
- `POST /api/tickets/{id}/generate/` - Generar boleto (admin)

## 🧪 Tests Unitarios

### Ejecutar Tests

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

## 📚 Documentación

### Swagger UI
Accede a la documentación interactiva en:
- **URL**: `http://127.0.0.1:8000/swagger/`
- **Funcionalidades**: Probar endpoints directamente
- **Autenticación**: Login integrado con JWT

### Estructura de la API
```
/api/
├── flights/          # Gestión de vuelos
├── passengers/       # Gestión de pasajeros
├── reservations/     # Sistema de reservas
├── planes/           # Gestión de aviones
├── tickets/          # Sistema de boletos
└── auth/             # Autenticación JWT
```

## 📁 Estructura del Proyecto

```
aerolinea/
├── gestionVuelos/
│   ├── models.py          # Modelos de datos
│   ├── views_api.py       # API REST endpoints
│   ├── serializers.py     # Serializers para API
│   ├── tests_api.py      # Tests unitarios
│   ├── urls_api.py       # URLs de la API
│   ├── views.py          # Vistas web
│   ├── urls.py           # URLs web
│   └── templates/        # Templates HTML
├── aerolinea/
│   ├── settings.py        # Configuración Django
│   └── urls.py           # URLs principales
├── home/                 # App de autenticación
├── requirements.txt      # Dependencias
└── README.md            # Este archivo
```

## 🔐 Autenticación

### Web (Sesiones)
- Login tradicional con usuario/contraseña
- Sesiones persistentes
- Logout automático

### API (JWT)
- Tokens de acceso (30 minutos)
- Tokens de refresh (1 día)
- Autenticación por header `Authorization: Bearer <token>`

### Permisos
- **Administradores**: Acceso completo a todas las funcionalidades
- **Usuarios**: Acceso limitado a consultas y reservas propias

## 🚀 Comandos Útiles

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

# Cargar datos de prueba
python manage.py loaddata fixtures/datos_prueba.json
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

## 📊 Funcionalidades Implementadas

### ✅ Gestión de Vuelos
- [x] Listar vuelos disponibles
- [x] Crear/editar/eliminar vuelos
- [x] Buscar vuelos por criterios
- [x] Gestionar pasajeros por vuelo

### ✅ Gestión de Pasajeros
- [x] Registro de pasajeros
- [x] Consulta de información
- [x] Historial de reservas
- [x] Validaciones de datos

### ✅ Sistema de Reservas
- [x] Crear reservas
- [x] Seleccionar asientos
- [x] Confirmar/cancelar reservas
- [x] Verificar disponibilidad

### ✅ Gestión de Aviones
- [x] Administrar flota
- [x] Layout de asientos
- [x] Verificar disponibilidad
- [x] Tipos de asientos

### ✅ Sistema de Boletos
- [x] Generar boletos
- [x] Consultar por código
- [x] Validaciones de estado
- [x] Códigos únicos

### ✅ API REST
- [x] Endpoints completos
- [x] Autenticación JWT
- [x] Permisos y roles
- [x] Filtros y búsquedas
- [x] Documentación Swagger

### ✅ Testing
- [x] Tests unitarios
- [x] Tests de autenticación
- [x] Tests de permisos
- [x] Cobertura completa

## 🎯 Resumen del Proyecto

- **Total de tests**: 13 ✅
- **Cobertura**: Endpoints API completos
- **Autenticación**: JWT implementada
- **Permisos**: Admin vs Usuario normal
- **Estado**: ✅ Todos los tests pasando
- **Documentación**: Swagger UI integrado

## 👨‍💻 Desarrollado por

**Estudiante de Ingeniería**  
**Fecha**: 2024  
**Proyecto**: Sistema de Gestión de Vuelos

---

¡El proyecto está completo y listo para usar! 🚀
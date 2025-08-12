# ✈️ Gestión Vuelos

Sistema web de gestión para una aerolínea, desarrollado en **Django** con **Bootstrap 5**, que permite administrar vuelos, pasajeros, reservas, aviones, tickets y reportes.  
Incluye autenticación de usuarios y una interfaz responsiva y moderna.

## 🚀 Características
- Gestión completa de **vuelos**, **pasajeros**, **reservas** y **aviones**.
- Generación de **tickets** y **reportes**.
- Sistema de **login, registro y logout**.
- Interfaz responsiva con **Bootstrap 5**.
- Panel de administración de Django para gestión avanzada.

## 🛠️ Tecnologías utilizadas
- [Python 3.x](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [SQLite / PostgreSQL](https://www.postgresql.org/)
- HTML5, CSS3 y JavaScript

## 📦 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone git@github.com:Cdruetta/EFI-ing-Aerolinea.git
   cd EFI-ing-Aerolinea
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor**
   ```bash
   python manage.py runserver
   ```

## 💻 Uso
- Accede a `http://localhost:8000/` para usar la interfaz.
- Accede a `http://localhost:8000/admin/` para el panel administrativo.

## 📸 Capturas de pantalla
*(Agrega aquí imágenes de las vistas más importantes)*

## 📜 Licencia
Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
# EFI-ing-Aerolinea

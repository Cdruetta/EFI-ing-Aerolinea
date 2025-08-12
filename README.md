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

1. Clonar el repositorio
   ```bash
   git clone git@github.com:Cdruetta/EFI-ing-Aerolinea.git
   cd EFI-ing-Aerolinea
Crear y activar entorno virtual

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instalar dependencias

bash
Copiar
Editar
pip install -r requirements.txt
Aplicar migraciones a la base de datos

bash
Copiar
Editar
python manage.py migrate
Crear superusuario

bash
Copiar
Editar
python manage.py createsuperuser
Iniciar el servidor

bash
Copiar
Editar
python manage.py runserver
💻 Uso
Acceder a la interfaz: http://localhost:8000/

Acceder al panel administrativo: http://localhost:8000/admin/

📸 Capturas de pantalla
(Agrega aquí imágenes de las vistas más importantes para mejor presentación)

🤝 Contribuciones
Las contribuciones son bienvenidas. Para contribuir, por favor:

Haz un fork del repositorio.

Crea una rama con tu feature (git checkout -b feature/nueva-funcionalidad).

Realiza commits claros y descriptivos.

Haz push a tu rama.

Abre un Pull Request describiendo tus cambios.

📝 Licencia
Este proyecto está bajo la licencia MIT - ver el archivo LICENSE para más detalles.

Autor: Cristian Eduardo Druetta
Contacto: c.druetta@itecriocuarto.org.ar

sql
Copiar
Editar

---

**LICENSE**

```text
MIT License

Copyright (c) 2025 Cristian Eduardo Druetta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

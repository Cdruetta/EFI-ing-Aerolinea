# ✈️ Gestión Vuelos

Sistema web para la gestión integral de una aerolínea, desarrollado con **Django** y **Bootstrap 5**. Permite administrar vuelos, pasajeros, reservas, aviones, tickets y reportes, incluyendo un sistema completo de autenticación de usuarios y una interfaz moderna y responsiva.

---

## 🚀 Características principales

- Gestión completa de **vuelos**, **pasajeros**, **reservas** y **aviones**.  
- Emisión de **tickets** y generación de **reportes** detallados.  
- Sistema de **registro, login y logout** para usuarios.  
- Interfaz responsiva y atractiva basada en **Bootstrap 5**.  
- Acceso al panel de administración estándar de Django para gestión avanzada.  

---

## 🛠️ Tecnologías utilizadas

- [Python 3.x](https://www.python.org/)  
- [Django](https://www.djangoproject.com/)  
- [Bootstrap 5](https://getbootstrap.com/)  
- Base de datos: [SQLite](https://www.sqlite.org/) por defecto / opción para PostgreSQL  
- Frontend: HTML5, CSS3, JavaScript  

---

## 📦 Instalación y puesta en marcha

1. Clonar el repositorio:

   ```bash
   git clone git@github.com:Cdruetta/EFI-ing-Aerolinea.git
   cd EFI-ing-Aerolinea
Crear y activar un entorno virtual:

bash
Copiar
Editar
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
Instalar las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Aplicar las migraciones de la base de datos:

bash
Copiar
Editar
python manage.py migrate
Crear un superusuario para acceder al panel administrativo:

bash
Copiar
Editar
python manage.py createsuperuser
Iniciar el servidor de desarrollo:

bash
Copiar
Editar
python manage.py runserver
💻 Uso
Accede a la aplicación web en:
http://localhost:8000/

Accede al panel administrativo de Django:
http://localhost:8000/admin/

📸 Capturas de pantalla
(Aquí puedes agregar imágenes o GIFs que muestren las funcionalidades principales del sistema para facilitar la comprensión visual.)

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Para colaborar:

Haz un fork del repositorio.

Crea una rama para tu feature:

bash
Copiar
Editar
git checkout -b feature/nueva-funcionalidad
Realiza commits claros y descriptivos.

Haz push a tu rama:

bash
Copiar
Editar
git push origin feature/nueva-funcionalidad
Abre un Pull Request explicando los cambios realizados.

📝 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

Autor
Cristian Eduardo Druetta
Correo: c.druetta@itecriocuarto.org.ar

LICENSE

text
Copiar
Editar
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
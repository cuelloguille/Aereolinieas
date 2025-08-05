# ✈️ Sistema de Gestión de Aerolíneas

Este proyecto está desarrollado en **Django** y permite gestionar vuelos, reservas y usuarios para una aerolínea. Ofrece una interfaz para usuarios y un panel de administración para el staff.

---

## 🚀 Características principales

- Registro, inicio y cierre de sesión de usuarios  
- Panel administrativo para gestión completa (vuelos, aviones, pasajeros, reservas)  
- Visualización de vuelos disponibles  
- Reserva y cancelación de vuelos  
- Roles de usuario diferenciados (administrador y cliente)  
- Validaciones de datos y manejo de errores  
- Uso opcional de Bootstrap para estilos  

---

## 🧰 Tecnologías utilizadas

- Python 3  
- Django 4.x  
- Bootstrap 5 (opcional)  
- SQLite (base de datos por defecto)  

---

## 📂 Estructura del proyecto

```plaintext
aerolinea/           # Configuración general de Django  
core/                # Aplicaciones:  vuelos, reservas, etc.  
templates/           # Plantillas HTML  

⚙️ Instalación y puesta en marcha
1. Clonar el repositorio
bash
Copiar
Editar
git clone https://github.com/cuelloguille/Aereolinieas.git
cd Aereolinieas
2. Crear y activar entorno virtual (recomendado)
Linux/macOS:

bash
Copiar
Editar
python3 -m venv env
source env/bin/activate
Windows:

bash
Copiar
Editar
python -m venv env
.\env\Scripts\activate
3. Instalar dependencias
bash
Copiar
Editar
pip install -r requirements.txt
Si no existe el archivo requirements.txt, instalá Django manualmente:

bash
Copiar
Editar
pip install django
4. Aplicar migraciones
bash
Copiar
Editar
python manage.py makemigrations
python manage.py migrate
5. Crear superusuario
bash
Copiar
Editar
python manage.py createsuperuser
6. Ejecutar servidor local
bash
Copiar
Editar
python manage.py runserver
7. Acceder a la aplicación
App principal: http://127.0.0.1:8000/

Panel admin: http://127.0.0.1:8000/admin/


📖 Descripción del proyecto
Este proyecto está diseñado para gestionar una aerolínea, con un enfoque claro en la experiencia tanto del administrador como del usuario final. La aplicación permite a los administradores controlar y gestionar todos los aspectos operativos del sistema, mientras que los usuarios pueden consultar vuelos y realizar reservas de manera sencilla y segura.

Funcionalidades para el Administrador
Gestión completa de vuelos: Crear, modificar y eliminar vuelos disponibles, incluyendo detalles como origen, destino, horarios y precios.

Administración de aviones y asientos: Controlar la flota de aviones y configurar la disponibilidad y características de los asientos para cada vuelo.

Gestión de reservas y pasajeros: Visualizar, aprobar, cancelar o modificar reservas realizadas por los usuarios, así como gestionar la información de los pasajeros.

Control de usuarios y roles: Crear y administrar cuentas de usuario, asignando roles (administrador o cliente) para controlar el acceso a diferentes funcionalidades.

Acceso al panel administrativo: Usar el panel de administración de Django para tener una vista centralizada y poderosa del sistema, facilitando tareas administrativas y reportes.

Funcionalidades para el Usuario
Registro e inicio de sesión: Crear una cuenta personal para acceder al sistema y gestionar sus reservas.

Consulta de vuelos disponibles: Visualizar fácilmente la lista de vuelos con información clara y detallada para planificar su viaje.

Reserva de vuelos: Seleccionar un vuelo y reservar un asiento disponible, con confirmación instantánea.

Cancelación de reservas: Permitir al usuario cancelar sus reservas de manera sencilla, liberando los asientos para otros pasajeros.

Gestión de perfil: Actualizar sus datos personales y visualizar el historial de reservas realizadas.

Objetivo
El objetivo principal es brindar una solución completa y funcional para la gestión de aerolíneas que pueda ser utilizada tanto como base para proyectos académicos o personales, como para adaptarse a necesidades reales del negocio. El sistema se enfoca en la seguridad, usabilidad y una arquitectura clara que facilite futuras ampliaciones y mejoras.
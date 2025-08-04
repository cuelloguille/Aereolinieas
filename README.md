# ✈️ Sistema de Gestión de Aerolíneas

Este es un proyecto web desarrollado con **Django** para gestionar una aerolínea. El sistema permite administrar vuelos, reservas, usuarios, aviones y más, desde dos tipos de vista: una para administradores y otra para usuarios comunes.

## 🚀 Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Panel de administración completo (vía Django admin)
- Visualización de vuelos disponibles
- Reserva y cancelación de vuelos
- Gestión de aviones, asientos, boletos y pasajeros
- Control de roles de usuario (admin y cliente)

## 🧰 Tecnologías utilizadas

- Python 3
- Django 4
- HTML/CSS
- Bootstrap (opcional para estilos)

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio


git clone https://github.com/cuelloguille/Aereolinieas.git
cd Aereolinieas
2. Crear y activar el entorno virtual
En Windows:
bash
Copiar
Editar
python -m venv env
env\Scripts\activate
En Linux/Mac:
bash
Copiar
Editar
python3 -m venv env
source env/bin/activate

3. Instalar dependencias
bash
Copiar
Editar
pip install -r requirements.txt


5. Aplicar migraciones
bash
Copiar
Editar
python manage.py makemigrations
python manage.py migrate

6. Crear superusuario (para acceder al panel admin)
bash
Copiar
Editar
python manage.py createsuperuser

7. Ejecutar el servidor
bash
Copiar
Editar
python manage.py runserver
Luego accedé a:

http://127.0.0.1:8000/ para ver la app.

http://127.0.0.1:8000/admin/ para ingresar al panel de administración.

http://127.0.0.1:8000/Vuelos/ para ingresar al  home

🙋‍♂️ Usuarios y roles
Administrador: Puede gestionar vuelos, usuarios, aviones, asientos, etc.

Usuario registrado: Puede registrarse, iniciar sesión, ver vuelos , reservar y candelar.

📁 Estructura general del proyecto
aerolinea/: configuración principal del proyecto Django.

apps/: contiene las aplicaciones de Django que gestionan vuelos, usuarios, reservas, etc.

templates/: vistas HTML del proyecto.

static/: archivos CSS y JS (si aplica).

📌 Notas
Asegurate de tener Python 3 y pip instalados antes de comenzar.

Podés adaptar o ampliar el sistema agregando nuevas funcionalidades como pasarelas de pago, notificaciones por email, etc.


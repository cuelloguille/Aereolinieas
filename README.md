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
apps/                # Aplicaciones: core, vuelos, reservas, etc.  
templates/           # Plantillas HTML  
static/              # Archivos estáticos (CSS, JS, imágenes)  
```

---

## ⚙️ Instalación y puesta en marcha

### 1. Clonar el repositorio

```bash
git clone https://github.com/cuelloguille/Aereolinieas.git
cd Aereolinieas
```

### 2. Crear y activar entorno virtual (recomendado)

Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```

Windows:
```bash
python -m venv env
.\env\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

*Si no existe el archivo `requirements.txt`, instalá Django manualmente:*

```bash
pip install django
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor local

```bash
python manage.py runserver
```

### 7. Acceder a la aplicación

- App principal: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
- Panel admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
- Página vuelos: [http://127.0.0.1:8000/vuelos/](http://127.0.0.1:8000/vuelos/)  

---

## 🙋‍♂️ Usuarios y roles

| Rol             | Funciones principales                              |
|-----------------|---------------------------------------------------|
| Administrador   | Gestión total: vuelos, usuarios, aviones, reservas|
| Usuario Cliente | Registro, inicio de sesión, ver vuelos, reservar y cancelar|

---

## 📝 Notas adicionales

- El proyecto está preparado para usarse en desarrollo (DEBUG=True).  
- Para producción, ajustar configuración de seguridad y base de datos.  
- Puedes extenderlo integrando pasarelas de pago, email, o APIs externas.  

---

"""
Django settings for aerolinea project.
"""

from pathlib import Path

# BASE_DIR: ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Seguridad
# ==============================
SECRET_KEY = 'django-insecure-fk$zhlny_sb4-yj%8+f0=@dwfa3a1l-fo(^t%adtfk-ik5ssbx'
DEBUG = True
ALLOWED_HOSTS = []   # Agrega dominios/ips en producción

# ==============================
# Aplicaciones instaladas
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps locales
    'core',
]

# ==============================
# Middleware
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================
# URLs y WSGI
# ==============================
ROOT_URLCONF = 'aerolinea.urls'

WSGI_APPLICATION = 'aerolinea.wsgi.application'

# ==============================
# Templates
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Puedes agregar aquí tu carpeta global de templates si la usas
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================
# Base de datos
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================
# Validación de contraseñas
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# Internacionalización
# ==============================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==============================
# Archivos estáticos
# ==============================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# ==============================
# Usuario personalizado
# ==============================
AUTH_USER_MODEL = 'core.Usuario'

# ==============================
# Autenticación (login/logout)
# ==============================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'vuelos_list'
LOGOUT_REDIRECT_URL = 'login'

# ==============================
# Clave primaria por defecto
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

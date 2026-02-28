"""
Django settings for ticketsystem project.
"""

from pathlib import Path
import os
import dj_database_url

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# SEGURIDAD
# ==============================

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-clave-de-desarrollo-123")

DEBUG = True 

ALLOWED_HOSTS = ['*']


# ==============================
# APLICACIONES (INSTALLED_APPS)
# ==============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tu aplicación de boletos
    'boletos',
]


# ==============================
# MIDDLEWARE
# ==============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'ticketsystem.urls'


# ==============================
# TEMPLATES
# ==============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
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


WSGI_APPLICATION = 'ticketsystem.wsgi.application'


# ==============================
# BASE DE DATOS (PostgreSQL Render)
# ==============================

DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://ticketsystem_db_utvu_user:oN6kiz4wRBBrUeRrh9ptU4Hst4sMYURu@dpg-d6ge1phdrdic73c4e8q0-a.oregon-postgres.render.com/ticketsystem_db_utvu"
)

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}


# ==============================
# VALIDADORES DE CONTRASEÑA
# ==============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================
# INTERNACIONALIZACIÓN
# ==============================

LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True


# ==============================
# ARCHIVOS ESTÁTICOS
# ==============================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================
# CONFIGURACIÓN ADICIONAL
# ==============================

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://*.ngrok-free.app",
    "https://ticketsystem-e3ww.onrender.com",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
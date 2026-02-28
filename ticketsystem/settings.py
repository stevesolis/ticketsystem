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

# En producción (Render), usa una variable de entorno. Localmente usa la clave por defecto.
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-clave-de-desarrollo-123")

# DEBUG debe ser True solo durante pruebas. En producción real, cámbialo a False.
DEBUG = True 

# Permitir todos los hosts para evitar errores de conexión con Ngrok y Render
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos estáticos en Render
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Opcional: si tienes templates globales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib
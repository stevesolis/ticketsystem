from django.contrib import admin
from django.urls import path
from boletos.views import home  # Importamos la función desde tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # La raíz ahora llama a la función en views.py
]
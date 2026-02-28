from django.urls import path
from . import views

urlpatterns = [
    # Usamos <uuid:codigo> porque tu código tiene formato de UUID
    # Si falla, podemos usar <path:codigo> que acepta cualquier caracter
    path('', views.inicio, name='inicio'), # Esta es la página de inicio pública
    path('validar/<path:codigo>/', views.validar_boleto, name='validar_boleto'),
    path('dashboard/', views.estadisticas, name='dashboard'),
]

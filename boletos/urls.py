from django.urls import path
from . import views

urlpatterns = [
    # Usamos <uuid:codigo> porque tu código tiene formato de UUID
    # Si falla, podemos usar <path:codigo> que acepta cualquier caracter
    path('validar/<path:codigo>/', views.validar_boleto, name='validar_boleto'),
    path('dashboard/', views.estadisticas, name='dashboard'),
]
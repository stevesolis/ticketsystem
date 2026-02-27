from django.urls import path
from .views import validar_boleto

urlpatterns = [
    path('validar/<uuid:codigo>/', validar_boleto, name='validar_boleto'),
]
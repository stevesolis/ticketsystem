from django.urls import path
from . import views

urlpatterns = [
    path('', views.validar_boleto, name='validar_boleto'),
]
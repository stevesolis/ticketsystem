from django.urls import path
from . import views

urlpatterns = [
    path("ver/<uuid:codigo>/", views.ver_boleto, name="ver_boleto"),
    path("validar/<uuid:codigo>/", views.confirmar_validacion, name="confirmar_validacion"),
]
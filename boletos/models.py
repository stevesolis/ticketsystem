import uuid
from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()

    def __str__(self):
        return self.nombre


class Boleto(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombre_asistente = models.CharField(max_length=200)
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_asistente} - {self.codigo}"
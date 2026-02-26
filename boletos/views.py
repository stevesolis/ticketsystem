import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
from .models import Evento, Boleto
from django.http import HttpResponse

def crear_boleto(request):
    evento = Evento.objects.first()

    if not evento:
        return render(request, "boletos/error.html", {
            "mensaje": "No hay eventos creados."
        })

    boleto = Boleto.objects.create(
        evento=evento,
        nombre_asistente="Steve Solis"
    )

    # Generar QR
    qr_data = f"http://192.168.1.10:8000/boletos/validar/{boleto.codigo}/"
    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "boletos/boleto.html", {
        "codigo": boleto.codigo,
        "qr_image": qr_base64
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from boletos.models import Boleto


def ver_boleto(request, codigo):
    boleto = get_object_or_404(Boleto, codigo=codigo)

    return render(request, "boletos/ver_boleto.html", {
        "boleto": boleto
    })


@login_required
def confirmar_validacion(request, codigo):
    boleto = get_object_or_404(Boleto, codigo=codigo)

    if not boleto.usado:
        boleto.usado = True
        boleto.fecha_ingreso = timezone.now()
        boleto.save()

    return redirect("ver_boleto", codigo=codigo)
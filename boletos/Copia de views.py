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

def validar_boleto(request, codigo):
    try:
        boleto = Boleto.objects.get(codigo=codigo)

        if boleto.usado:
            return HttpResponse("<h2 style='color:red;'>❌ Boleto ya utilizado</h2>")

        boleto.usado = True
        boleto.save()

        return HttpResponse("<h2 style='color:green;'>✅ Acceso permitido</h2>")

    except Boleto.DoesNotExist:
        return HttpResponse("<h2 style='color:red;'>❌ Boleto inválido</h2>")
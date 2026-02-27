import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import Evento, Boleto

def crear_boleto(request):
    # Intentamos obtener el primer evento o devolvemos error si no existe
    evento = Evento.objects.first()

    if not evento:
        return render(request, "boletos/error.html", {
            "mensaje": "No hay eventos creados. Por favor, crea uno en el admin."
        })

    # Creamos el registro del boleto
    boleto = Boleto.objects.create(
        evento=evento,
        nombre_asistente="Steve Solis" # Aquí podrías usar datos de un formulario
    )

    # DINÁMICO: Obtenemos el dominio actual (Render o Local)
    # Esto evita que el QR falle al cambiar de servidor
    domain = request.build_absolute_uri('/')[:-1] 
    qr_data = f"{domain}/validar/{boleto.codigo}/"
    
    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir imagen a Base64 para mostrarla en el HTML
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "boletos/boleto.html", {
        "boleto": boleto,
        "qr_image": qr_base64
    })

def ver_boleto(request, codigo):
    """Vista para que el asistente vea su boleto."""
    boleto = get_object_or_404(Boleto, codigo=codigo)
    return render(request, "boletos/ver_boleto.html", {
        "boleto": boleto
    })

@login_required
def confirmar_validacion(request, codigo):
    """Vista protegida para que el staff marque el boleto como usado."""
    boleto = get_object_or_404(Boleto, codigo=codigo)

    if not boleto.usado:
        boleto.usado = True
        boleto.fecha_ingreso = timezone.now()
        boleto.save()

    return redirect("ver_boleto", codigo=codigo)
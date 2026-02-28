import os
import qrcode
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from boletos.models import Boleto

class Command(BaseCommand):
    help = 'Generar imágenes de boletos con QR que apuntan a la URL de Ngrok'

    def handle(self, *args, **kwargs):
        # --- CONFIGURACIÓN DE NGROK ---
        # 1. Ejecuta en tu terminal: ngrok http 8000
        # 2. Copia la URL que dice "Forwarding" (ejemplo: https://1a2b-3c4d.ngrok-free.app)
        # 3. Pégala aquí abajo asegurándote de que termine en /validar/
        
        BASE_URL = "https://ticketsystem-e3ww.onrender.com/validar/"

        base_path = "assets/base_boleto.png"
        output_root = "boletos_generados"

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        # Obtenemos todos los boletos de la base de datos
        boletos = Boleto.objects.all().order_by("nombre_asistente")
        contador_global = 0

        for boleto in boletos:
            contador_global += 1
            numero = contador_global
            
            # Limpiar nombre para crear las carpetas individuales
            nombre_original = boleto.nombre_asistente
            nombre_limpio = unicodedata.normalize('NFKD', nombre_original).encode('ASCII', 'ignore').decode()
            nombre_carpeta = nombre_limpio.strip().replace(" ", "_")

            carpeta_persona = os.path.join(output_root, nombre_carpeta)
            if not os.path.exists(carpeta_persona):
                os.makedirs(carpeta_persona)

            # --- GENERACIÓN DE QR CON URL DE NGROK ---
            # El QR ahora será: https://xxxx.ngrok-free.app/validar/UUID-DEL-BOLETO/
            url_validacion = f"{BASE_URL}{boleto.codigo}/"
            qr = qrcode.make(url_validacion)
            qr = qr.resize((400, 400))

            # --- PROCESAMIENTO DE IMAGEN ---
            try:
                base = Image.open(base_path).convert("RGBA")
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"No se encontró la base en {base_path}"))
                return

            # Pegar el QR en las coordenadas indicadas
            qr_x, qr_y = 2450, 2500
            base.paste(qr, (qr_x, qr_y))

            draw = ImageDraw.Draw(base)
            
            # Carga de fuente (Mantengo tu lógica original)
            try:
                # Si estás en Mac usa esta ruta, en Windows sería "arial.ttf"
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 60)
            except:
                font = ImageFont.load_default()

            # Texto del número de boleto
            texto = f"EVT-2025-{numero:03d}"
            text_width = draw.textlength(texto, font=font)
            text_x = qr_x + (400 - text_width) / 2 
            text_y = qr_y + 410

            draw.text((text_x, text_y), texto, fill="black", font=font)

            # Guardar el resultado
            output_path = os.path.join(carpeta_persona, f"boleto_{numero:03d}.png")
            base.save(output_path)

        self.stdout.write(
            self.style.SUCCESS(f"¡Éxito! {contador_global} boletos generados apuntando a Ngrok: {BASE_URL}")
        )
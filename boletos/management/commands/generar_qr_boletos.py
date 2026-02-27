import os
import qrcode
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from boletos.models import Boleto

class Command(BaseCommand):
    help = 'Generar imágenes de boletos agrupados por carpeta pero con numeración global única'

    def handle(self, *args, **kwargs):
        base_path = "assets/base_boleto.png"
        output_root = "boletos_generados"

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        # Obtenemos todos los boletos
        boletos = Boleto.objects.all().order_by("nombre_asistente")

        # --- CAMBIO CLAVE: Un solo contador para todos ---
        contador_global = 0 

        for boleto in boletos:
            # Incrementamos el contador en cada iteración del bucle principal
            contador_global += 1
            numero = contador_global

            nombre_original = boleto.nombre_asistente

            # Limpiar nombre para carpeta
            nombre_limpio = unicodedata.normalize('NFKD', nombre_original)
            nombre_limpio = nombre_limpio.encode('ASCII', 'ignore').decode()
            nombre_carpeta = nombre_limpio.strip().replace(" ", "_")

            carpeta_persona = os.path.join(output_root, nombre_carpeta)

            if not os.path.exists(carpeta_persona):
                os.makedirs(carpeta_persona)

            # Generar QR
            qr = qrcode.make(str(boleto.codigo))
            qr = qr.resize((400, 400))

            base = Image.open(base_path).convert("RGBA")

            qr_x = 2450
            qr_y = 2500
            base.paste(qr, (qr_x, qr_y))

            draw = ImageDraw.Draw(base)

            try:
                # Nota: Asegúrate de que esta ruta sea válida en tu servidor/PC
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 45)
            except:
                font = ImageFont.load_default()

            # El formato :03d pondrá ceros a la izquierda (001, 002, etc.)
            texto = f"EVT-2025-{numero:03d}"

            text_width = draw.textlength(texto, font=font)
            text_x = qr_x + (350 - text_width) / 2
            text_y = qr_y + 390

            draw.text((text_x, text_y), texto, fill="black", font=font)

            # El nombre del archivo ahora usará el número global
            output_path = os.path.join(
                carpeta_persona,
                f"boleto_{numero:03d}.png"
            )

            base.save(output_path)

        self.stdout.write(self.style.SUCCESS(f"Generados {contador_global} boletos con numeración única."))
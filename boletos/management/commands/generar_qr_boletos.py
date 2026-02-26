import os
import qrcode
import unicodedata
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from boletos.models import Boleto


class Command(BaseCommand):
    help = 'Generar imágenes de boletos agrupados y numerados por persona'

    def handle(self, *args, **kwargs):

        base_path = "assets/base_boleto.png"
        output_root = "boletos_generados"

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        boletos = Boleto.objects.all().order_by("nombre_asistente")

        contador_por_persona = defaultdict(int)

        for boleto in boletos:

            nombre_original = boleto.nombre_asistente

            # Limpiar nombre para carpeta
            nombre_limpio = unicodedata.normalize('NFKD', nombre_original)
            nombre_limpio = nombre_limpio.encode('ASCII', 'ignore').decode()
            nombre_carpeta = nombre_limpio.strip().replace(" ", "_")

            carpeta_persona = os.path.join(output_root, nombre_carpeta)

            if not os.path.exists(carpeta_persona):
                os.makedirs(carpeta_persona)

            # Incrementar contador por persona
            contador_por_persona[nombre_original] += 1
            numero = contador_por_persona[nombre_original]

            # Generar QR
            qr = qrcode.make(str(boleto.codigo))
            qr = qr.resize((300, 300))

            base = Image.open(base_path).convert("RGBA")

            qr_x = 800
            qr_y = 400
            base.paste(qr, (qr_x, qr_y))

            draw = ImageDraw.Draw(base)

            try:
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 45)
            except:
                font = ImageFont.load_default()

            texto = f"{numero:03d}"

            text_width = draw.textlength(texto, font=font)
            text_x = qr_x + (300 - text_width) / 2
            text_y = qr_y + 320

            draw.text((text_x, text_y), texto, fill="black", font=font)

            output_path = os.path.join(
                carpeta_persona,
                f"boleto_{numero:03d}.png"
            )

            base.save(output_path)

        self.stdout.write(self.style.SUCCESS("Boletos generados correctamente por persona"))
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from boletos.models import Boleto


class Command(BaseCommand):
    help = 'Generar imágenes de boletos con QR'

    def handle(self, *args, **kwargs):

        base_path = "assets/base_boleto.png"
        output_folder = "boletos_generados"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        boletos = Boleto.objects.all()

        for index, boleto in enumerate(boletos, start=1):

            # Generar QR
            qr = qrcode.make(str(boleto.codigo))
            qr = qr.resize((500, 500))

            # Abrir imagen base
            base = Image.open(base_path).convert("RGBA")

            # Posición QR
            qr_x = 800
            qr_y = 400
            base.paste(qr, (qr_x, qr_y))

            # Dibujar texto
            draw = ImageDraw.Draw(base)

            # Intentar usar fuente más profesional
            try:
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 45)
            except:
                font = ImageFont.load_default()

            # Texto de numeración (ej: Boleto #001)
            texto = f"EVT-2025-{index:03d}"

            # Centrar debajo del QR
            text_width = draw.textlength(texto, font=font)
            text_x = qr_x + (300 - text_width) / 2
            text_y = qr_y + 320

            draw.text((text_x, text_y), texto, fill="black", font=font)

            # Guardar
            output_path = f"{output_folder}/boleto_{boleto.codigo}.png"
            base.save(output_path)

        self.stdout.write(self.style.SUCCESS("Boletos generados correctamente con numeración"))
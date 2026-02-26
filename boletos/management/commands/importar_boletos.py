import csv
from django.core.management.base import BaseCommand
from boletos.models import Evento, Boleto

class Command(BaseCommand):
    help = 'Importar boletos desde CSV'

    def handle(self, *args, **kwargs):
        evento = Evento.objects.first()

        if not evento:
            self.stdout.write(self.style.ERROR("No hay evento creado"))
            return

        with open('boletos.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            total_generados = 0

            for row in reader:
                responsable = row['responsable']
                cantidad = int(row['cantidad'])

                for i in range(cantidad):
                    Boleto.objects.create(
                        evento=evento,
                        nombre_asistente=responsable
                    )
                    total_generados += 1

        self.stdout.write(self.style.SUCCESS(f"Se generaron {total_generados} boletos correctamente"))
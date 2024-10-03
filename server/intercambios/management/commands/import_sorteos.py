import csv
import re
from datetime import datetime

from django.core.management.base import BaseCommand
from intercambios.models import Sorteo


# python manage.py import_sorteos path/to/sorteos.csv
class Command(BaseCommand):
    help = "Importa sorteos desde un archivo CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Ruta al archivo CSV")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        success_count = 0
        total_rows = 0
        error_count = 0

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1
                try:
                    # Extract and validate fields
                    fecha = self.parse_fecha(
                        row.get("FECHA") or row.get("fecha"), total_rows
                    )
                    codigo = self.construct_codigo(
                        row.get("Nº") or row.get("codigo"), fecha, total_rows
                    )
                    precio = self.parse_precio(
                        row.get("PRECIO") or row.get("precio"), total_rows
                    )

                    # Update or create the Sorteo record
                    sorteo, created = Sorteo.objects.update_or_create(
                        codigo=codigo,
                        defaults={
                            "fecha": fecha,
                            "precio": precio,
                            # Add other fields here if necessary
                        },
                    )

                    # Provide feedback
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"[Fila {total_rows}] Sorteo '{codigo}' creado."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"[Fila {total_rows}] Sorteo '{codigo}' actualizado."
                            )
                        )

                    success_count += 1

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"[Fila {total_rows}] Error: {e}")
                    )
                    continue  # Skip to the next row

        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\nImportación completada. {success_count}/{total_rows} filas procesadas correctamente."
            )
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"{error_count} filas tuvieron errores y fueron omitidas."
                )
            )

    def parse_fecha(self, fecha_str, row_number):
        if not fecha_str:
            raise ValueError(f"Fecha vacía en la fila {row_number}.")
        try:
            # Assuming the date format is 'DD/MM/YYYY'
            return datetime.strptime(fecha_str.strip(), "%d/%m/%y").date()
        except ValueError:
            raise ValueError(
                f"Formato de fecha inválido en la fila {row_number}: '{fecha_str}'."
            )

    def construct_codigo(self, numero_str, fecha, row_number):
        if not numero_str:
            raise ValueError(f"Número de sorteo vacío en la fila {row_number}.")
        year = fecha.year
        codigo = f"{numero_str.strip()}/{year}"
        if len(codigo.split("/")) != 2:
            raise ValueError(f"Código inválido en la fila {row_number}: '{codigo}'.")
        return codigo

    def parse_precio(self, precio_str, row_number):
        if not precio_str:
            raise ValueError(f"Precio vacío en la fila {row_number}.")
        # Remove currency symbols and spaces, replace commas with dots
        precio_clean = re.sub(r"[^\d,\.]", "", precio_str).replace(",", ".")
        try:
            return float(precio_clean)
        except ValueError:
            raise ValueError(
                f"Precio inválido en la fila {row_number}: '{precio_str}'."
            )

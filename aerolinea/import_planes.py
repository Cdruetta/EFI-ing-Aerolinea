import csv
import os
import django
from datetime import datetime

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aerolinea.settings')
django.setup()

from gestionVuelos.models import Passenger

# Ruta al archivo CSV
csv_file_path = 'pasajeros_ejemplo.csv'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            full_name = row['Nombre completo']
            document_type = row['Tipo de Documento']
            document_number = row['Número de Documento']
            email = row['Email']
            phone = row['Teléfono']
            birth_date = datetime.strptime(row['Fecha de Nacimiento'], "%d/%m/%Y").date()

            passenger, created = Passenger.objects.get_or_create(
                document_number=document_number,
                defaults={
                    'full_name': full_name,
                    'document_type': document_type,
                    'email': email,
                    'phone': phone,
                    'birth_date': birth_date,
                }
            )

            if created:
                print(f'✅ Pasajero creado: {full_name}')
            else:
                print(f'ℹ️ Pasajero ya existía: {full_name}')

        except Exception as e:
            print(f'❌ Error con fila: {row}')
            print(f'   {e}')

print('✔️ Importación finalizada.')

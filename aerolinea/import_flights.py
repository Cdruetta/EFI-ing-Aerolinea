import csv
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aerolinea.settings')
django.setup()

from gestionVuelos.models import Plane, Flight

def str_to_timedelta(time_str):
    h, m, s = map(int, time_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

csv_file_path = 'flights_ejemplo.csv'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            plane = Plane.objects.get(model=row['plane_model'])
        except Plane.DoesNotExist:
            print(f"Avión modelo '{row['plane_model']}' no encontrado. Se omite este vuelo.")
            continue

        departure_time = datetime.strptime(row['departure_time'], '%Y-%m-%d %H:%M')
        arrival_time = datetime.strptime(row['arrival_time'], '%Y-%m-%d %H:%M')
        duration = str_to_timedelta(row['duration'])

        flight, created = Flight.objects.get_or_create(
            plane=plane,
            origin=row['origin'],
            destination=row['destination'],
            departure_time=departure_time,
            arrival_time=arrival_time,
            defaults={
                'duration': duration,
                'status': row['status'],
                'base_price': float(row['base_price']),
            }
        )

        if created:
            print(f"Vuelo {row['origin']} → {row['destination']} creado.")
        else:
            print(f"Vuelo {row['origin']} → {row['destination']} ya existe.")

print("Importación de vuelos finalizada.")

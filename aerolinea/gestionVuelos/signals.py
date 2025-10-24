from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from gestionVuelos.models import Passenger
import uuid

@receiver(post_save, sender=User)
def create_passenger_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Verificar si hay datos de pasajero en la sesión
        # Como las señales no tienen acceso directo a la sesión,
        # usaremos un enfoque diferente: crear el pasajero con datos temporales
        # y luego actualizarlo desde la vista
        
        # Generar un número de documento temporal único
        temp_document_number = f"TEMP_{instance.id}_{str(uuid.uuid4())[:8]}"
        
        Passenger.objects.create(
            user=instance,
            full_name=instance.username, 
            document_number=temp_document_number,   
            email=instance.email or '',
            phone='',
            birth_date='1900-01-01',
            document_type=Passenger.DNI
        )

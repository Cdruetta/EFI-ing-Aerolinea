from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from gestionVuelos.models import Passenger

@receiver(post_save, sender=User)
def create_passenger_for_new_user(sender, instance, created, **kwargs):
    if created:
        Passenger.objects.create(
            user=instance,
            full_name=instance.username, 
            document_number="00000000",   
            email=instance.email or '',
            phone='',
            birth_date='1900-01-01',
            document_type=Passenger.DNI
        )

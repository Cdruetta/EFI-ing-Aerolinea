from django.shortcuts import get_object_or_404

from gestionVuelos.models import Passenger
from datetime import date

class PassengerRepository:
    @staticmethod
    def get_all() -> list[Passenger]:
        return list(Passenger.objects.all()) 

    @staticmethod
    def get_by_id(passenger_id: int) -> Passenger:
        return get_object_or_404(Passenger, id=passenger_id)

    @staticmethod
    def create(
        full_name: str,
        document_number: str,
        email: str,
        phone: str,
        birth_date: date,
        document_type: str
    ) -> Passenger:
        passenger = Passenger(
            full_name=full_name,
            document_number=document_number,
            email=email,
            phone=phone,
            birth_date=birth_date,
            document_type=document_type
        )
        passenger.save()
        return passenger

    @staticmethod
    def update(
        passenger: Passenger,
        full_name: str,
        document_number: str,
        email: str,
        phone: str,
        birth_date: date,
        document_type: str
    ) -> Passenger:
        passenger.full_name = full_name
        passenger.document_number = document_number
        passenger.email = email
        passenger.phone = phone
        passenger.birth_date = birth_date
        passenger.document_type = document_type
        passenger.save()
        return passenger

    @staticmethod
    def delete(passenger_id: int) -> bool:
        try:
            Passenger.objects.get(id=passenger_id).delete()
            return True
        except Passenger.DoesNotExist:
            return False

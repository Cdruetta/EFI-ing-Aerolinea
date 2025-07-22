from typing import List, Optional
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from gestionVuelos.models import Passenger, Reservation
from gestionVuelos.repositories.passenger import PassengerRepository


class PassengerService:

    @staticmethod
    def get_all() -> List[Passenger]:
        return list(PassengerRepository.get_all())

    @staticmethod
    def get_all_with_reservations() -> List[Passenger]:
        reservations_with_flights = Reservation.objects.select_related('flight')
        return list(
            Passenger.objects.prefetch_related(
                Prefetch('reservation_set', queryset=reservations_with_flights)
            ).all()
        )

    @staticmethod
    def get_by_id(passenger_id: int) -> Optional[Passenger]:
        return PassengerRepository.get_by_id(passenger_id)

    @staticmethod
    def create(
        full_name: str,
        document_number: str,
        email: str,
        phone: str,
        birth_date,
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
        passenger.full_clean()
        passenger.save()
        return passenger

    @staticmethod
    def update(
        passenger_id: int,
        full_name: str,
        document_number: str,
        email: str,
        phone: str,
        birth_date,
        document_type: str
    ) -> bool:
        try:
            passenger = PassengerRepository.get_by_id(passenger_id)
            if not passenger:
                return False
            passenger.full_name = full_name
            passenger.document_number = document_number
            passenger.email = email
            passenger.phone = phone
            passenger.birth_date = birth_date
            passenger.document_type = document_type
            passenger.full_clean()
            passenger.save()
            return True
        except Passenger.DoesNotExist:
            return False

    @staticmethod
    def delete(passenger_id: int) -> bool:
        passenger = PassengerRepository.get_by_id(passenger_id)
        if passenger:
            passenger.delete()
            return True
        return False

from typing import List
from django.shortcuts import get_object_or_404

from gestionVuelos.models import Flight, Passenger, Reservation, Seat
from gestionVuelos.repositories.reservations import ReservationRepository
from decimal import Decimal


class ReservationService:
    """
        def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def get_all(self) -> List[Reservation]:
        return list(Reservation.objects.all())
    """
    
    @staticmethod
    def get_all():
        return list(ReservationRepository.get_all())
    
    @staticmethod
    def delete(reservation_id: int) -> bool:
        reservation = ReservationRepository.get_by_id(reservation_id=reservation_id)
        if reservation:
            reservation.delete()
            return True
        return False

    @staticmethod
    def update(
        reservation_id: int,
        flight_id: int,
        passenger_id: int,
        seat_id: int,
        status: str,
        price: float,
        reservation_code: str
    ) -> bool:
        try:
            reservation = ReservationRepository.get_by_id(reservation_id)
            if not reservation:
                return False
            
            flight = get_object_or_404(Flight, id=flight_id)
            passenger = get_object_or_404(Passenger, id=passenger_id)
            seat = get_object_or_404(Seat, id=seat_id)
            
            reservation.flight = flight
            reservation.passenger = passenger
            reservation.seat = seat
            reservation.status = status
            reservation.price = price
            reservation.reservation_code = reservation_code
            
            reservation.save()
            return True
        except Reservation.DoesNotExist:
            return False
            
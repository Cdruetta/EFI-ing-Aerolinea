from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

from gestionVuelos.models import Reservation
from datetime import datetime
from decimal import Decimal

class ReservationRepository:
    @staticmethod
    def get_all() -> QuerySet[Reservation]:
        """
            Obtiene todos los objetos (reservas)
        """
        return Reservation.objects.all()
            


    @staticmethod
    def get_by_id(reservation_id: int) -> Reservation:
        return get_object_or_404(Reservation, id=reservation_id)

    @staticmethod
    def create(
        flight,
        passenger,
        seat,
        status: str,
        price: Decimal,
        reservation_code: str,
    ) -> Reservation:
        reservation = Reservation(
            flight=flight,
            passenger=passenger,
            seat=seat,
            status=status,
            price=price,
            reservation_code=reservation_code,
        )
        reservation.save()
        return reservation

    @staticmethod
    def update(
        reservation: Reservation,
        flight,
        passenger,
        seat,
        status: str,
        price: Decimal,
        reservation_code: str,
    ) -> Reservation:
        reservation.flight = flight
        reservation.passenger = passenger
        reservation.seat = seat
        reservation.status = status
        reservation.price = price
        reservation.reservation_code = reservation_code
        reservation.save()
        return reservation

    @staticmethod
    def delete(reservation_id: int) -> bool:
        try:
            Reservation.objects.get(id=reservation_id).delete()
            return True
        except Reservation.DoesNotExist:
            return False

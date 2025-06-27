from django.shortcuts import get_object_or_404

from gestionVuelos.models import Seat


class SeatRepository:

    @staticmethod
    def get_all() -> list[Seat]:
        return list(Seat.objects.all())

    @staticmethod
    def get_by_id(seat_id: int) -> Seat:
        return get_object_or_404(Seat, id=seat_id)

    @staticmethod
    def create(number: int, plane) -> Seat:
        seat = Seat(number=number, plane=plane)
        seat.save()
        return seat

    @staticmethod
    def update(
        seat: Seat,
        number: str,
        row: int,
        column: str,
        seat_type: str,
        status: str,
        plane
    ) -> Seat:
        seat.number = number
        seat.row = row
        seat.column = column
        seat.seat_type = seat_type
        seat.status = status
        seat.plane = plane
        seat.save()
        return seat


    @staticmethod
    def delete(seat_id: int) -> bool:
        try:
            Seat.objects.get(id=seat_id).delete()
            return True
        except Seat.DoesNotExist:
            return False

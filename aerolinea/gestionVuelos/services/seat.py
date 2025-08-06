from typing import List, Optional
from django.shortcuts import get_object_or_404
from gestionVuelos.models import Seat, Plane
from gestionVuelos.repositories.seat import SeatRepository

class SeatService:

    @staticmethod
    def get_all() -> List[Seat]:
        return list(SeatRepository.get_all())

    @staticmethod
    def get_by_id(seat_id: int) -> Optional[Seat]:
        return SeatRepository.get_by_id(seat_id)

    @staticmethod
    def create(
        plane_id: int,
        number: str,
        row: int,
        column: str,
        seat_type: str,
        status: str = 'available'
    ) -> Seat:
        plane = get_object_or_404(Plane, id=plane_id)
        seat = Seat(
            plane=plane,
            number=number,
            row=row,
            column=column,
            seat_type=seat_type,
            status=status
        )
        seat.full_clean()
        seat.save()
        return seat

    @staticmethod
    def update(
        seat_id: int,
        plane_id: int,
        number: str,
        row: int,
        column: str,
        seat_type: str,
        status: str
    ) -> bool:
        try:
            seat = SeatRepository.get_by_id(seat_id)
            if not seat:
                return False
            plane = get_object_or_404(Plane, id=plane_id)
            seat.plane = plane
            seat.number = number
            seat.row = row
            seat.column = column
            seat.seat_type = seat_type
            seat.status = status
            seat.full_clean()
            seat.save()
            return True
        except Seat.DoesNotExist:
            return False

    @staticmethod
    def delete(seat_id: int) -> bool:
        seat = SeatRepository.get_by_id(seat_id)
        if seat:
            seat.delete()
            return True
        return False

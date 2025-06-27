from typing import List, Optional
from gestionVuelos.models import Plane
from gestionVuelos.repositories.planes import PlaneRepository

class PlaneService:

    @staticmethod
    def get_all() -> List[Plane]:
        return list(PlaneRepository.get_all())

    @staticmethod
    def get_by_id(plane_id: int) -> Optional[Plane]:
        return PlaneRepository.get_by_id(plane_id)

    @staticmethod
    def create(
        model: str,
        capacity: int,
        available_seats: int
    ) -> Plane:
        plane = Plane(
            model=model,
            capacity=capacity,
            available_seats=available_seats
        )
        plane.full_clean()
        plane.save()
        return plane

    @staticmethod
    def update(
        plane_id: int,
        model: str,
        capacity: int,
        available_seats: int
    ) -> bool:
        try:
            plane = PlaneRepository.get_by_id(plane_id)
            if not plane:
                return False
            plane.model = model
            plane.capacity = capacity
            plane.available_seats = available_seats
            plane.full_clean()
            plane.save()
            return True
        except Plane.DoesNotExist:
            return False

    @staticmethod
    def delete(plane_id: int) -> bool:
        plane = PlaneRepository.get_by_id(plane_id)
        if plane:
            plane.delete()
            return True
        return False

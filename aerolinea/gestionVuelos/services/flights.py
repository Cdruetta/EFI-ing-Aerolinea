from typing import List, Optional
from django.shortcuts import get_object_or_404

from gestionVuelos.models import Flight, Plane
from gestionVuelos.repositories.flights import FlightRepository

class FlightService:

    @staticmethod
    def get_all() -> List[Flight]:
        return list(FlightRepository.get_all())

    @staticmethod
    def get_by_id(flight_id: int) -> Optional[Flight]:
        return FlightRepository.get_by_id(flight_id)

    @staticmethod
    def create(
        plane_id: int,
        origin: str,
        destination: str,
        departure_time,
        arrival_time,
        duration,
        status: str,
        base_price: float
    ) -> Flight:
        plane = get_object_or_404(Plane, id=plane_id)
        flight = Flight(
            plane=plane,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            status=status,
            base_price=base_price
        )
        flight.full_clean()
        flight.save()
        return flight

    @staticmethod
    def update(
        flight_id: int,
        plane_id: int,
        origin: str,
        destination: str,
        departure_time,
        arrival_time,
        duration,
        status: str,
        base_price: float
    ) -> bool:
        try:
            flight = FlightRepository.get_by_id(flight_id)
            if not flight:
                return False
            plane = get_object_or_404(Plane, id=plane_id)
            flight.plane = plane
            flight.origin = origin
            flight.destination = destination
            flight.departure_time = departure_time
            flight.arrival_time = arrival_time
            flight.duration = duration
            flight.status = status
            flight.base_price = base_price
            flight.full_clean()
            flight.save()
            return True
        except Flight.DoesNotExist:
            return False

    @staticmethod
    def delete(flight_id: int) -> bool:
        flight = FlightRepository.get_by_id(flight_id)
        if flight:
            flight.delete()
            return True
        return False

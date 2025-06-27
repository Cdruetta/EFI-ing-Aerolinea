from django.shortcuts import get_object_or_404

from gestionVuelos.models import Flight
from datetime import datetime, timedelta
from decimal import Decimal

class FlightRepository:
    @staticmethod
    def get_all() -> list[Flight]:
        return list(Flight.objects.all())

    @staticmethod
    def get_by_id(flight_id: int) -> Flight:
        return get_object_or_404(Flight, id=flight_id)

    @staticmethod
    def create(
        plane,
        origin: str,
        destination: str,
        departure_time: datetime,
        arrival_time: datetime,
        duration: timedelta,
        status: str,
        base_price: Decimal,
    ) -> Flight:
        flight = Flight(
            plane=plane,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            status=status,
            base_price=base_price,
        )
        flight.save()
        return flight

    @staticmethod
    def update(
        flight: Flight,
        plane,
        origin: str,
        destination: str,
        departure_time: datetime,
        arrival_time: datetime,
        duration: timedelta,
        status: str,
        base_price: Decimal,
    ) -> Flight:
        flight.plane = plane
        flight.origin = origin
        flight.destination = destination
        flight.departure_time = departure_time
        flight.arrival_time = arrival_time
        flight.duration = duration
        flight.status = status
        flight.base_price = base_price
        flight.save()
        return flight

    @staticmethod
    def delete(flight_id: int) -> bool:
        try:
            Flight.objects.get(id=flight_id).delete()
            return True
        except Flight.DoesNotExist:
            return False

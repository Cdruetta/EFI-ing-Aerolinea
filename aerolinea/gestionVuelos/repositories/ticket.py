from django.shortcuts import get_object_or_404

from gestionVuelos.models import Ticket
from datetime import datetime
import uuid

class TicketRepository:
    @staticmethod
    def get_all() -> list[Ticket]:
        return list(Ticket.objects.all())  

    @staticmethod
    def get_by_id(ticket_id: int) -> Ticket:
        return get_object_or_404(Ticket, id=ticket_id)

    @staticmethod
    def create(
        reservation,
        status: str = "issued",
        barcode: str | None = None,
    ) -> Ticket:
        ticket = Ticket(
            reservation=reservation,
            status=status,
        )
        if barcode is not None:
            ticket.barcode = barcode
        ticket.save()
        return ticket

    @staticmethod
    def update(
        ticket: Ticket,
        reservation,
        status: str,
        barcode: str | None = None,
    ) -> Ticket:
        ticket.reservation = reservation
        ticket.status = status
        if barcode is not None:
            ticket.barcode = barcode
        ticket.save()
        return ticket

    @staticmethod
    def delete(ticket_id: int) -> bool:
        try:
            Ticket.objects.get(id=ticket_id).delete()
            return True
        except Ticket.DoesNotExist:
            return False

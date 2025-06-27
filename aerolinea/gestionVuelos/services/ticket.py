from typing import List, Optional
from django.shortcuts import get_object_or_404

from gestionVuelos.models import Ticket, Reservation
from gestionVuelos.repositories.ticket import TicketRepository
import uuid

class TicketService:

    @staticmethod
    def get_all() -> List[Ticket]:
        return list(TicketRepository.get_all())

    @staticmethod
    def get_by_id(ticket_id: int) -> Optional[Ticket]:
        return TicketRepository.get_by_id(ticket_id)

    @staticmethod
    def create(
        reservation_id: int,
        barcode: str | None = None,
        status: str = "issued"
    ) -> Ticket:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        ticket = Ticket(
            reservation=reservation,
            status=status
        )
        if barcode:
            ticket.barcode = barcode
        else:
            ticket.barcode = str(uuid.uuid4()).replace("-", "").upper()
        ticket.full_clean()
        ticket.save()
        return ticket

    @staticmethod
    def update(
        ticket_id: int,
        reservation_id: int,
        barcode: str,
        status: str
    ) -> bool:
        try:
            ticket = TicketRepository.get_by_id(ticket_id)
            if not ticket:
                return False
            reservation = get_object_or_404(Reservation, id=reservation_id)
            ticket.reservation = reservation
            ticket.barcode = barcode
            ticket.status = status
            ticket.full_clean()
            ticket.save()
            return True
        except Ticket.DoesNotExist:
            return False

    @staticmethod
    def delete(ticket_id: int) -> bool:
        ticket = TicketRepository.get_by_id(ticket_id)
        if ticket:
            ticket.delete()
            return True
        return False

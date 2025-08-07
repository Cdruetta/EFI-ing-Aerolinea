from django.contrib import admin

# Register your models here.
from gestionVuelos.models import Flight, Passenger, Seat, Reservation, Ticket, Plane


@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "capacity", "available_seats")
    list_filter = ("capacity",)
    search_fields = ("model",)

    def available_seats(self, obj):
        return obj.seat_set.filter(status='available').count()
    available_seats.short_description = "Available Seats"


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "plane",
        "origin",
        "destination",
        "departure_time",
        "arrival_time",
        "duration",
        "status",
        "base_price",
    )
    list_filter = ("plane", "status")
    search_fields = ("origin", "destination", "status")


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "document_number",
        "email",
        "phone",
        "birth_date",
        "document_type",
    )
    list_filter = ("document_type", "birth_date")
    search_fields = (
        "full_name",
        "document_number",
        "email",
        "phone",
        "birth_date",
        "document_type",
    )


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "row", "column", "seat_type", "status", "plane")
    list_filter = ("status", "plane")
    search_fields = ("number", "row", "column", "seat_type")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "flight",
        "passenger",
        "seat",
        "status",
        "reservation_date",
        "price",
        "reservation_code",
    )
    list_filter = ("flight", "passenger", "seat", "status")
    search_fields = ("flight", "passenger", "seat", "status", "reservation_code")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "barcode",
        "get_flight",
        "get_passenger",
        "get_seat",
        "reservation",
        "status",
        "issued_at",
    )
    list_filter = (
        "status",
        "reservation__flight",
        "reservation__passenger",
        "reservation__seat",
    )
    search_fields = (
        "reservation__flight__code",
        "reservation__passenger__full_name",
        "reservation__seat__number",
        "reservation__reservation_code",
    )

    def get_flight(self, obj):
        return obj.reservation.flight

    get_flight.short_description = "Flight"

    def get_passenger(self, obj):
        return obj.reservation.passenger

    get_passenger.short_description = "Passenger"

    def get_seat(self, obj):
        return obj.reservation.seat

    get_seat.short_description = "Seat"

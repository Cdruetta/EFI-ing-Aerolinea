from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid


class Plane(models.Model):
    manufacturer = models.CharField(max_length=100, default="Desconocido")
    model = models.CharField(max_length=30)
    capacity = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.manufacturer} {self.model} - {self.capacity} seats"


class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("occupied", "Occupied"),
    ]

    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    number = models.CharField(max_length=5)
    row = models.IntegerField()
    column = models.CharField(max_length=1)
    seat_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default="available")

    def __str__(self):
        return f"Seat {self.number} ({self.status})"


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    DNI = "DNI"
    PASSPORT = "Pasaporte"
    DOCUMENT_TYPE_CHOICES = [
        (DNI, "DNI"),
        (PASSPORT, "Pasaporte"),
    ]

    full_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, default=DNI)

    def __str__(self):
        return f"{self.full_name} - {self.document_number}"


class Flight(models.Model):
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_time})"


class Reservation(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("cancelled", "Cancelled"),
    ]

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default="reserved")
    reservation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reservation_code = models.CharField(max_length=20, unique=True, blank=True)

    def clean(self):
        if self.seat.plane != self.flight.plane:
            raise ValidationError("The selected seat does not belong to the plane of the flight.")

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            self.reservation_code = str(uuid.uuid4()).replace("-", "")[:20].upper()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation {self.reservation_code} - {self.passenger.full_name}"


class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ("issued", "Issued"),
        ("cancelled", "Cancelled"),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, unique=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default="issued")

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = str(uuid.uuid4()).replace("-", "").upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket - {self.reservation.reservation_code}"

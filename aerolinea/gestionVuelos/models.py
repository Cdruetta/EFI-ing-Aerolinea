from django.db import models
from django.core.exceptions import ValidationError


import uuid


# class avión
class Plane(models.Model):
    manufacturer = models.CharField(max_length=100,  default='Desconocido')
    model = models.CharField(max_length=30)  # Nombre o código del modelo del avión
    capacity = models.IntegerField()  # Capacidad total de asientos
    available_seats = (
        models.IntegerField()
    )  # Asientos disponibles (puede actualizarse según reservas)

    def __str__(self):
        return f"{self.manufacturer} {self.model} - {self.capacity} seats"


# class asiento dentro de un avión
class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ("available", "Available"),  # Disponible para reservar
        ("reserved", "Reserved"),  # Ya reservado
        ("occupied", "Occupied"),  # Ya ocupado
    ]

    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)  # Relación con un avión
    number = models.CharField(max_length=5)  # Número de asiento (ej: 12A)
    row = models.IntegerField()  # Fila del asiento
    column = models.CharField(max_length=1)  # Columna del asiento (ej: A, B, C)
    seat_type = models.CharField(
        max_length=50
    )  # Tipo de asiento (ventana, pasillo, etc.)
    status = models.CharField(
        max_length=20, choices=SEAT_STATUS_CHOICES, default="available"
    )  # Estado actual del asiento

    def __str__(self):
        return f"Seat {self.number} ({self.status})"


# clase pasajero
class Passenger(models.Model):
    full_name = models.CharField(max_length=100)  # Nombre completo
    document_number = models.CharField(max_length=50, unique=True)  # Documento único
    email = models.EmailField()  # Email de contacto
    phone = models.CharField(max_length=20)  # Número de teléfono
    birth_date = models.DateField()  # Fecha de nacimiento
    document_type = models.CharField(
        max_length=50
    )  # Tipo de documento (DNI, pasaporte, etc.)

    def __str__(self):
        return f"{self.full_name} - {self.document_number}"


# clase vuelo
class Flight(models.Model):
    plane = models.ForeignKey(
        Plane, on_delete=models.CASCADE
    )  # Avión asignado al vuelo
    origin = models.CharField(max_length=100)  # Ciudad o aeropuerto de origen
    destination = models.CharField(max_length=100)  # Ciudad o aeropuerto de destino
    departure_time = models.DateTimeField()  # Fecha y hora de salida
    arrival_time = models.DateTimeField()  # Fecha y hora de llegada
    duration = models.DurationField()  # Duración estimada del vuelo
    status = models.CharField(
        max_length=50
    )  # Estado del vuelo (programado, retrasado, etc.)
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Precio base del boleto

    def clean(self):
        # Validación para asegurar que la llegada sea después de la salida
        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama automáticamente a clean() antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_time})"


# clase reserva
class Reservation(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("cancelled", "Cancelled"),
    ]

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Vuelo reservado
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE
    )  # Pasajero que reserva
    seat = models.OneToOneField(
        Seat, on_delete=models.CASCADE
    )  # Asiento asignado (uno a uno)
    status = models.CharField(
        max_length=20, choices=RESERVATION_STATUS_CHOICES, default="reserved"
    )  # Estado de la reserva
    reservation_date = models.DateTimeField(
        auto_now_add=True
    )  # Fecha y hora de creación de la reserva
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio final
    reservation_code = models.CharField(
        max_length=20, unique=True
    )  # Código único de reserva

    def clean(self):
        # Validación: el asiento debe pertenecer al avión del vuelo reservado
        if self.seat.plane != self.flight.plane:
            raise ValidationError(
                "The selected seat does not belong to the plane of the flight."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation {self.reservation_code} - {self.passenger.full_name}"


# clase boleto
import uuid  # Asegurate de importar uuid arriba del archivo


class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ("issued", "Issued"),
        ("cancelled", "Cancelled"),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    barcode = models.CharField(
        max_length=100, unique=True, blank=True
    )  # Permitimos blank para auto-generar
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=TICKET_STATUS_CHOICES, default="issued"
    )

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = str(uuid.uuid4()).replace("-", "").upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket - {self.reservation.reservation_code}"

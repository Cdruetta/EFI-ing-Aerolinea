from rest_framework import serializers
from .models import Flight, Passenger, Reservation, Plane, Ticket

# ----------------------------
# Serializer de Plane
# ----------------------------
class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad del avión debe ser mayor a 0")
        return value

# ----------------------------
# Serializer de Flight
# ----------------------------
class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer(read_only=True)
    plane_id = serializers.PrimaryKeyRelatedField(
        queryset=Plane.objects.all(), source='plane', write_only=True
    )

    class Meta:
        model = Flight
        fields = [
            'id', 'origin', 'destination', 'departure_time',
            'arrival_time', 'duration', 'status', 'base_price',
            'plane', 'plane_id'
        ]

    def validate_departure_time(self, value):
        from datetime import datetime
        if value < datetime.now():
            raise serializers.ValidationError("La fecha/hora de salida no puede ser anterior a ahora")
        return value

# ----------------------------
# Serializer de Passenger
# ----------------------------
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'full_name', 'document_type', 'document_number', 'email', 'phone', 'birth_date']

    def validate_document_number(self, value):
        if not value.isdigit() or len(value) < 7:
            raise serializers.ValidationError("Número de documento inválido")
        return value

# ----------------------------
# Serializer de Reservation
# ----------------------------
class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(read_only=True)
    passenger_id = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), source='passenger', write_only=True
    )

    flight = FlightSerializer(read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), source='flight', write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            'id', 'passenger', 'passenger_id',
            'flight', 'flight_id', 'seat', 'status', 'reservation_date', 'price', 'reservation_code'
        ]

    def validate_seat(self, value):
        if not value:
            raise serializers.ValidationError("Debe seleccionar un asiento")
        return value

    def validate(self, data):
        flight = data.get('flight')
        seat = data.get('seat')
        if flight and flight.reservations.filter(seat=seat, status='reserved').exists():
            raise serializers.ValidationError("El asiento ya está reservado en este vuelo")
        return data

# ----------------------------
# Serializer de Ticket
# ----------------------------
class TicketSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(), source='reservation', write_only=True
    )

    class Meta:
        model = Ticket
        fields = ['id', 'barcode', 'reservation', 'reservation_id', 'issued_at', 'status']

    def validate_reservation(self, value):
        if value.status != 'reserved':
            raise serializers.ValidationError("Solo se pueden generar tickets para reservas confirmadas")
        return value

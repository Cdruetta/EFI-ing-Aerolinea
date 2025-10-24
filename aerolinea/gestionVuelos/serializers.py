# -*- coding: utf-8 -*-
"""
Serializers para el sistema de gestion de vuelos
Desarrollado por: [Nombre del Estudiante]
Fecha: 2024
"""

from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date
from .models import Flight, Passenger, Reservation, Plane, Seat, Ticket

# =============================================================================
# SERIALIZER DE AVIONES
# =============================================================================

class PlaneSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Plane
    """
    class Meta:
        model = Plane
        fields = '__all__'

    def validate_capacity(self, value):
        """
        Validar que la capacidad sea mayor a 0
        """
        if value <= 0:
            raise serializers.ValidationError("La capacidad del avión debe ser mayor a 0")
        if value > 1000:
            raise serializers.ValidationError("La capacidad del avión no puede ser mayor a 1000")
        return value

    def validate_model(self, value):
        """
        Validar que el modelo no esté vacío
        """
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("El modelo del avión debe tener al menos 2 caracteres")
        return value.strip()

# =============================================================================
# SERIALIZER DE ASIENTOS
# =============================================================================

class SeatSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Seat
    """
    class Meta:
        model = Seat
        fields = '__all__'

    def validate_number(self, value):
        """
        Validar formato del número de asiento
        """
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError("El número de asiento no puede estar vacío")
        return value.strip()

    def validate_row(self, value):
        """
        Validar que la fila sea positiva
        """
        if value <= 0:
            raise serializers.ValidationError("La fila debe ser mayor a 0")
        return value

    def validate(self, data):
        """
        Validaciones cruzadas
        """
        plane = data.get('plane')
        row = data.get('row')
        column = data.get('column')
        
        if plane and row and column:
            # Verificar que no exista otro asiento con el mismo número en el mismo avión
            existing_seat = Seat.objects.filter(
                plane=plane, 
                number=data.get('number')
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_seat.exists():
                raise serializers.ValidationError(
                    f"Ya existe un asiento con el número {data.get('number')} en este avión"
                )
        
        return data

# =============================================================================
# SERIALIZER DE VUELOS
# =============================================================================

class FlightSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Flight
    """
    plane = PlaneSerializer(read_only=True)
    plane_id = serializers.PrimaryKeyRelatedField(
        queryset=Plane.objects.all(), 
        source='plane', 
        write_only=True,
        help_text="ID del avión asignado al vuelo"
    )
    available_seats = serializers.SerializerMethodField(read_only=True)
    total_seats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'origin', 'destination', 'departure_time',
            'arrival_time', 'duration', 'status', 'base_price',
            'plane', 'plane_id', 'available_seats', 'total_seats'
        ]

    def get_available_seats(self, obj):
        """
        Obtener número de asientos disponibles
        """
        return obj.seats_available()

    def get_total_seats(self, obj):
        """
        Obtener número total de asientos
        """
        return obj.plane.capacity

    def validate_departure_time(self, value):
        """
        Validar que la fecha de salida no sea en el pasado
        """
        if value < timezone.now():
            raise serializers.ValidationError("La fecha/hora de salida no puede ser anterior a ahora")
        return value

    def validate_arrival_time(self, value):
        """
        Validar que la fecha de llegada sea posterior a la de salida
        """
        departure_time = self.initial_data.get('departure_time')
        if departure_time:
            try:
                departure = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
                if value <= departure:
                    raise serializers.ValidationError("La fecha de llegada debe ser posterior a la de salida")
            except ValueError:
                pass
        return value

    def validate(self, data):
        """
        Validaciones cruzadas
        """
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        
        if departure_time and arrival_time:
            if arrival_time <= departure_time:
                raise serializers.ValidationError("La fecha de llegada debe ser posterior a la de salida")
        
        return data

# =============================================================================
# SERIALIZER DE PASAJEROS
# =============================================================================

class PassengerSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Passenger
    """
    class Meta:
        model = Passenger
        fields = [
            'id', 'full_name', 'document_type', 'document_number', 
            'email', 'phone', 'birth_date'
        ]

    def validate_document_number(self, value):
        """
        Validar formato del número de documento
        """
        if not value or len(value.strip()) < 7:
            raise serializers.ValidationError("El número de documento debe tener al menos 7 caracteres")
        
        # Verificar que solo contenga números
        if not value.isdigit():
            raise serializers.ValidationError("El número de documento solo puede contener números")
        
        return value.strip()

    def validate_email(self, value):
        """
        Validar formato del email
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Debe proporcionar un email válido")
        return value.lower().strip()

    def validate_phone(self, value):
        """
        Validar formato del teléfono
        """
        if not value or len(value.strip()) < 8:
            raise serializers.ValidationError("El teléfono debe tener al menos 8 caracteres")
        return value.strip()

    def validate_birth_date(self, value):
        """
        Validar que la fecha de nacimiento sea válida
        """
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura")
        
        # Verificar que la persona tenga al menos 0 años (recién nacido)
        age = (date.today() - value).days // 365
        if age > 120:
            raise serializers.ValidationError("La edad no puede ser mayor a 120 años")
        
        return value

    def validate_full_name(self, value):
        """
        Validar formato del nombre completo
        """
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        
        # Verificar que contenga al menos un espacio (nombre y apellido)
        if ' ' not in value.strip():
            raise serializers.ValidationError("Debe proporcionar nombre y apellido")
        
        return value.strip().title()

# =============================================================================
# SERIALIZER DE RESERVAS
# =============================================================================

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Reservation
    """
    passenger = PassengerSerializer(read_only=True)
    passenger_id = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), 
        source='passenger', 
        write_only=True,
        help_text="ID del pasajero"
    )
    flight = FlightSerializer(read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), 
        source='flight', 
        write_only=True,
        help_text="ID del vuelo"
    )
    seat = SeatSerializer(read_only=True)
    seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(), 
        source='seat', 
        write_only=True,
        help_text="ID del asiento"
    )

    class Meta:
        model = Reservation
        fields = [
            'id', 'passenger', 'passenger_id', 'flight', 'flight_id',
            'seat', 'seat_id', 'status', 'reservation_date', 'price', 'reservation_code'
        ]
        read_only_fields = ['reservation_code', 'reservation_date']

    def validate_seat(self, value):
        """
        Validar que el asiento esté disponible
        """
        if not value:
            raise serializers.ValidationError("Debe seleccionar un asiento")
        
        if value.status != 'available':
            raise serializers.ValidationError("El asiento seleccionado no está disponible")
        
        return value

    def validate(self, data):
        """
        Validaciones cruzadas
        """
        flight = data.get('flight')
        seat = data.get('seat')
        
        if flight and seat:
            # Verificar que el asiento pertenezca al avión del vuelo
            if seat.plane != flight.plane:
                raise serializers.ValidationError(
                    "El asiento seleccionado no pertenece al avión de este vuelo"
                )
            
            # Verificar que el asiento no esté ya reservado en este vuelo
            existing_reservation = Reservation.objects.filter(
                flight=flight, 
                seat=seat, 
                status='reserved'
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_reservation.exists():
                raise serializers.ValidationError(
                    "El asiento ya está reservado en este vuelo"
                )
        
        return data

    def create(self, validated_data):
        """
        Crear reserva y actualizar estado del asiento
        """
        seat = validated_data['seat']
        
        # Crear la reserva
        reservation = super().create(validated_data)
        
        # Actualizar estado del asiento
        seat.status = 'reserved'
        seat.save()
        
        return reservation

# =============================================================================
# SERIALIZER DE BOLETOS
# =============================================================================

class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Ticket
    """
    reservation = ReservationSerializer(read_only=True)
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(), 
        source='reservation', 
        write_only=True,
        help_text="ID de la reserva"
    )

    class Meta:
        model = Ticket
        fields = [
            'id', 'barcode', 'reservation', 'reservation_id', 
            'issued_at', 'status'
        ]
        read_only_fields = ['barcode', 'issued_at']

    def validate_reservation(self, value):
        """
        Validar que la reserva esté confirmada
        """
        if value.status != 'reserved':
            raise serializers.ValidationError(
                "Solo se pueden generar boletos para reservas confirmadas"
            )
        
        # Verificar que no exista ya un boleto para esta reserva
        if hasattr(value, 'ticket'):
            raise serializers.ValidationError(
                "Ya existe un boleto para esta reserva"
            )
        
        return value

    def create(self, validated_data):
        """
        Crear boleto y generar código único
        """
        import uuid
        reservation = validated_data['reservation']
        
        # Generar código único para el boleto
        barcode = str(uuid.uuid4()).replace('-', '').upper()[:20]
        
        # Crear el boleto
        ticket = Ticket.objects.create(
            reservation=reservation,
            barcode=barcode
        )
        
        return ticket

# =============================================================================
# SERIALIZER PARA REPORTES
# =============================================================================

class FlightPassengersReportSerializer(serializers.Serializer):
    """
    Serializer para reporte de pasajeros por vuelo
    """
    flight_id = serializers.IntegerField()
    flight_origin = serializers.CharField()
    flight_destination = serializers.CharField()
    flight_departure_time = serializers.DateTimeField()
    total_passengers = serializers.IntegerField()
    passengers = PassengerSerializer(many=True)

class PassengerReservationsReportSerializer(serializers.Serializer):
    """
    Serializer para reporte de reservas de un pasajero
    """
    passenger_id = serializers.IntegerField()
    passenger_name = serializers.CharField()
    total_reservations = serializers.IntegerField()
    active_reservations = serializers.IntegerField()
    reservations = ReservationSerializer(many=True)
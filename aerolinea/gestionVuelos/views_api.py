# -*- coding: utf-8 -*-
"""
API Views para el sistema de gestion de vuelos
Desarrollado por: [Nombre del Estudiante]
Fecha: 2024
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, date

# Importar modelos y serializers
from .models import Flight, Passenger, Reservation, Plane, Seat, Ticket
from .serializers import (
    FlightSerializer,
    PassengerSerializer,
    ReservationSerializer,
    PlaneSerializer,
    SeatSerializer,
    TicketSerializer
)

# =============================================================================
# GESTIÓN DE VUELOS (API)
# =============================================================================

class FlightViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar vuelos
    Permite listar, crear, editar y eliminar vuelos
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['origin', 'destination', 'departure_time', 'status']
    search_fields = ['origin', 'destination']
    ordering_fields = ['departure_time', 'arrival_time', 'base_price']
    ordering = ['departure_time']

    def get_permissions(self):
        """
        Solo los administradores pueden crear, editar o eliminar vuelos
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        """
        Listar vuelos disponibles (no cancelados)
        """
        flights = self.get_queryset().filter(status__in=['scheduled', 'boarding'])
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        """
        Buscar vuelos por origen, destino y fecha
        """
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        departure_date = request.query_params.get('departure_date')
        
        queryset = self.get_queryset()
        
        if origin:
            queryset = queryset.filter(origin__icontains=origin)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if departure_date:
            try:
                date_obj = datetime.strptime(departure_date, '%Y-%m-%d').date()
                queryset = queryset.filter(departure_time__date=date_obj)
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def passengers(self, request, pk=None):
        """
        Obtener listado de pasajeros por vuelo (solo administradores)
        """
        flight = self.get_object()
        reservations = flight.reservations.filter(status='reserved').select_related(
            'passenger', 'seat'
        )
        
        passengers_data = []
        for reservation in reservations:
            passenger_data = {
                'passenger': {
                    'id': reservation.passenger.id,
                    'full_name': reservation.passenger.full_name,
                    'document_type': reservation.passenger.document_type,
                    'document_number': reservation.passenger.document_number,
                    'email': reservation.passenger.email,
                    'phone': reservation.passenger.phone,
                },
                'reservation': {
                    'id': reservation.id,
                    'reservation_code': reservation.reservation_code,
                    'reservation_date': reservation.reservation_date,
                    'price': reservation.price,
                    'status': reservation.status,
                },
                'seat': {
                    'id': reservation.seat.id,
                    'number': reservation.seat.number,
                    'row': reservation.seat.row,
                    'column': reservation.seat.column,
                    'seat_type': reservation.seat.seat_type,
                }
            }
            passengers_data.append(passenger_data)
        
        return Response({
            'flight': {
                'id': flight.id,
                'origin': flight.origin,
                'destination': flight.destination,
                'departure_time': flight.departure_time,
                'arrival_time': flight.arrival_time,
                'status': flight.status,
            },
            'total_passengers': len(passengers_data),
            'passengers': passengers_data
        })

# =============================================================================
# GESTIÓN DE PASAJEROS (API)
# =============================================================================

class PassengerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pasajeros
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'document_number', 'email']
    filterset_fields = ['document_type']

    def get_permissions(self):
        """
        Solo los administradores pueden crear, editar o eliminar pasajeros
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def reservations(self, request, pk=None):
        """
        Listar reservas asociadas a un pasajero
        """
        passenger = self.get_object()
        reservations = Reservation.objects.filter(
            passenger=passenger
        ).select_related('flight__plane', 'seat')
        
        reservations_data = []
        for reservation in reservations:
            reservation_data = {
                'id': reservation.id,
                'reservation_code': reservation.reservation_code,
                'reservation_date': reservation.reservation_date,
                'price': reservation.price,
                'status': reservation.status,
                'flight': {
                    'id': reservation.flight.id,
                    'origin': reservation.flight.origin,
                    'destination': reservation.flight.destination,
                    'departure_time': reservation.flight.departure_time,
                    'arrival_time': reservation.flight.arrival_time,
                    'duration': reservation.flight.duration,
                    'status': reservation.flight.status,
                    'base_price': reservation.flight.base_price,
                    'plane': {
                        'id': reservation.flight.plane.id,
                        'model': reservation.flight.plane.model,
                        'manufacturer': reservation.flight.plane.manufacturer,
                        'capacity': reservation.flight.plane.capacity,
                    }
                },
                'seat': {
                    'id': reservation.seat.id,
                    'number': reservation.seat.number,
                    'row': reservation.seat.row,
                    'column': reservation.seat.column,
                    'seat_type': reservation.seat.seat_type,
                    'status': reservation.seat.status,
                }
            }
            reservations_data.append(reservation_data)
        
        return Response({
            'passenger': {
                'id': passenger.id,
                'full_name': passenger.full_name,
                'document_number': passenger.document_number,
                'email': passenger.email,
            },
            'total_reservations': len(reservations_data),
            'reservations': reservations_data
        })

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def active_reservations(self, request, pk=None):
        """
        Obtener reservas activas de un pasajero
        """
        passenger = self.get_object()
        reservations = Reservation.objects.filter(
            passenger=passenger, 
            status='reserved'
        ).select_related('flight__plane', 'seat')
        
        reservations_data = []
        for reservation in reservations:
            reservation_data = {
                'id': reservation.id,
                'reservation_code': reservation.reservation_code,
                'reservation_date': reservation.reservation_date,
                'price': reservation.price,
                'status': reservation.status,
                'flight': {
                    'id': reservation.flight.id,
                    'origin': reservation.flight.origin,
                    'destination': reservation.flight.destination,
                    'departure_time': reservation.flight.departure_time,
                    'arrival_time': reservation.flight.arrival_time,
                    'duration': reservation.flight.duration,
                    'status': reservation.flight.status,
                    'base_price': reservation.flight.base_price,
                    'plane': {
                        'id': reservation.flight.plane.id,
                        'model': reservation.flight.plane.model,
                        'manufacturer': reservation.flight.plane.manufacturer,
                        'capacity': reservation.flight.plane.capacity,
                    }
                },
                'seat': {
                    'id': reservation.seat.id,
                    'number': reservation.seat.number,
                    'row': reservation.seat.row,
                    'column': reservation.seat.column,
                    'seat_type': reservation.seat.seat_type,
                    'status': reservation.seat.status,
                }
            }
            reservations_data.append(reservation_data)
        
        return Response({
            'passenger': {
                'id': passenger.id,
                'full_name': passenger.full_name,
                'document_number': passenger.document_number,
                'email': passenger.email,
            },
            'total_active_reservations': len(reservations_data),
            'reservations': reservations_data
        })

# =============================================================================
# SISTEMA DE RESERVAS (API)
# =============================================================================

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reservas
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['passenger', 'flight', 'status']
    ordering_fields = ['reservation_date', 'id']
    ordering = ['-reservation_date']

    def get_permissions(self):
        """
        Solo los administradores pueden eliminar reservas
        """
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check_seat(self, request):
        """
        Verificar disponibilidad de un asiento en un vuelo
        """
        flight_id = request.query_params.get('flight_id')
        seat_id = request.query_params.get('seat_id')
        
        if not flight_id or not seat_id:
            return Response(
                {'error': 'flight_id y seat_id son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {'error': 'Vuelo no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response(
                {'error': 'Asiento no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar si el asiento pertenece al avión del vuelo
        if seat.plane != flight.plane:
            return Response(
                {'error': 'El asiento no pertenece al avión de este vuelo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si está ocupado
        occupied = flight.reservations.filter(seat=seat, status='reserved').exists()
        
        return Response({
            'seat_id': seat_id,
            'available': not occupied,
            'seat_number': seat.number,
            'seat_type': seat.seat_type
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        """
        Confirmar una reserva
        """
        reservation = self.get_object()
        
        if reservation.status != 'reserved':
            return Response(
                {'error': 'Solo se pueden confirmar reservas en estado "reserved"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'confirmed'
        reservation.save()
        
        serializer = self.get_serializer(reservation)
        return Response({
            'message': 'Reserva confirmada exitosamente',
            'reservation': serializer.data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """
        Cancelar una reserva
        """
        reservation = self.get_object()
        
        if reservation.status == 'cancelled':
            return Response(
                {'error': 'La reserva ya está cancelada'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'cancelled'
        reservation.save()
        
        # Liberar el asiento
        seat = reservation.seat
        seat.status = 'available'
        seat.save()
        
        serializer = self.get_serializer(reservation)
        return Response({
            'message': 'Reserva cancelada exitosamente',
            'reservation': serializer.data
        })

# =============================================================================
# GESTIÓN DE AVIONES Y ASIENTOS (API)
# =============================================================================

class PlaneViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar aviones
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['model', 'manufacturer']

    def get_permissions(self):
        """
        Solo los administradores pueden crear, editar o eliminar aviones
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def seats(self, request, pk=None):
        """
        Obtener layout de asientos de un avión
        """
        plane = self.get_object()
        seats = Seat.objects.filter(plane=plane).order_by('row', 'column')
        
        seats_data = []
        for seat in seats:
            seat_data = {
                'id': seat.id,
                'number': seat.number,
                'row': seat.row,
                'column': seat.column,
                'seat_type': seat.seat_type,
                'status': seat.status
            }
            seats_data.append(seat_data)
        
        return Response({
            'plane': {
                'id': plane.id,
                'model': plane.model,
                'manufacturer': plane.manufacturer,
                'capacity': plane.capacity
            },
            'total_seats': len(seats_data),
            'seats': seats_data
        })

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def available_seats(self, request, pk=None):
        """
        Obtener asientos disponibles de un avión
        """
        plane = self.get_object()
        seats = Seat.objects.filter(plane=plane, status='available').order_by('row', 'column')
        
        seats_data = []
        for seat in seats:
            seat_data = {
                'id': seat.id,
                'number': seat.number,
                'row': seat.row,
                'column': seat.column,
                'seat_type': seat.seat_type,
                'status': seat.status
            }
            seats_data.append(seat_data)
        
        return Response({
            'plane': {
                'id': plane.id,
                'model': plane.model,
                'manufacturer': plane.manufacturer,
                'capacity': plane.capacity
            },
            'available_seats': len(seats_data),
            'seats': seats_data
        })

# =============================================================================
# GESTIÓN DE BOLETOS (API)
# =============================================================================

class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar boletos
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['issued_at', 'barcode']
    search_fields = ['barcode', 'reservation__reservation_code']
    ordering = ['-issued_at']

    def get_permissions(self):
        """
        Solo los administradores pueden crear, editar o eliminar boletos
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_barcode(self, request):
        """
        Consultar información de un boleto por código
        """
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response(
                {'error': 'El parámetro barcode es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ticket = Ticket.objects.select_related(
                'reservation__passenger',
                'reservation__flight__plane',
                'reservation__seat'
            ).get(barcode=barcode)
            
            ticket_data = {
                'id': ticket.id,
                'barcode': ticket.barcode,
                'status': ticket.status,
                'issued_at': ticket.issued_at,
                'reservation': {
                    'id': ticket.reservation.id,
                    'reservation_code': ticket.reservation.reservation_code,
                    'status': ticket.reservation.status,
                    'reservation_date': ticket.reservation.reservation_date,
                    'price': ticket.reservation.price,
                    'passenger': {
                        'id': ticket.reservation.passenger.id,
                        'full_name': ticket.reservation.passenger.full_name,
                        'document_type': ticket.reservation.passenger.document_type,
                        'document_number': ticket.reservation.passenger.document_number,
                        'email': ticket.reservation.passenger.email,
                        'phone': ticket.reservation.passenger.phone,
                        'birth_date': ticket.reservation.passenger.birth_date,
                    },
                    'flight': {
                        'id': ticket.reservation.flight.id,
                        'origin': ticket.reservation.flight.origin,
                        'destination': ticket.reservation.flight.destination,
                        'departure_time': ticket.reservation.flight.departure_time,
                        'arrival_time': ticket.reservation.flight.arrival_time,
                        'duration': ticket.reservation.flight.duration,
                        'status': ticket.reservation.flight.status,
                        'base_price': ticket.reservation.flight.base_price,
                        'plane': {
                            'id': ticket.reservation.flight.plane.id,
                            'model': ticket.reservation.flight.plane.model,
                            'manufacturer': ticket.reservation.flight.plane.manufacturer,
                            'capacity': ticket.reservation.flight.plane.capacity,
                        }
                    },
                    'seat': {
                        'id': ticket.reservation.seat.id,
                        'number': ticket.reservation.seat.number,
                        'row': ticket.reservation.seat.row,
                        'column': ticket.reservation.seat.column,
                        'seat_type': ticket.reservation.seat.seat_type,
                        'status': ticket.reservation.seat.status,
                    }
                }
            }
            
            return Response(ticket_data)
            
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'No se encontró un boleto con el código proporcionado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def generate(self, request, pk=None):
        """
        Generar boleto a partir de una reserva confirmada
        """
        reservation = self.get_object().reservation
        
        if reservation.status != 'reserved':
            return Response(
                {'error': 'Solo se pueden generar boletos de reservas confirmadas'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if hasattr(reservation, 'ticket'):
            return Response(
                {'error': 'Ya existe un boleto para esta reserva'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket = Ticket.objects.create(reservation=reservation)
        serializer = self.get_serializer(ticket)
        
        return Response({
            'message': 'Boleto generado exitosamente',
            'ticket': serializer.data
        }, status=status.HTTP_201_CREATED)
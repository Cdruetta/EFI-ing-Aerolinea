from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

# modelos y serializers
from .models import Flight, Passenger, Reservation, Plane, Ticket
from .serializers import (
    FlightSerializer,
    PassengerSerializer,
    ReservationSerializer,
    PlaneSerializer,
    TicketSerializer
)

# ----------------------------
# FlightViewSet
# ----------------------------
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['origin', 'destination', 'departure_time']
    search_fields = ['origin', 'destination']
    ordering_fields = ['departure_time', 'arrival_time']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    # Listado de pasajeros por vuelo (solo admins)
    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def passengers(self, request, pk=None):
        flight = self.get_object()
        reservations = flight.reservations.filter(status='reserved')
        passengers = [res.passenger for res in reservations]
        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)

# ----------------------------
# PassengerViewSet
# ----------------------------
class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'document_number', 'email']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    # Reservas activas de un pasajero (usuario autenticado)
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def active_reservations(self, request, pk=None):
        passenger = self.get_object()
        reservations = Reservation.objects.filter(passenger=passenger, status='reserved')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

# ----------------------------
# ReservationViewSet
# ----------------------------
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['passenger', 'flight', 'status']
    ordering_fields = ['id']

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    # Verificar disponibilidad de un asiento en un vuelo
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check_seat(self, request):
        flight_id = request.query_params.get('flight_id')
        seat_id = request.query_params.get('seat_id')
        if not flight_id or not seat_id:
            return Response({'error': 'flight_id y seat_id son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        occupied = flight.reservations.filter(seat_id=seat_id, status='reserved').exists()
        return Response({'seat_id': seat_id, 'available': not occupied})

    # Generar ticket desde reserva confirmada (solo admins)
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def generate_ticket(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status != 'reserved':
            return Response({'error': 'Solo se pueden generar tickets de reservas activas'}, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket.objects.create(reservation=reservation, barcode=str(reservation.id) + "-" + timezone.now().strftime("%Y%m%d%H%M%S"))
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ----------------------------
# PlaneViewSet
# ----------------------------
class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['model', 'manufacturer']

# ----------------------------
# TicketViewSet
# ----------------------------
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['issued_at', 'barcode']

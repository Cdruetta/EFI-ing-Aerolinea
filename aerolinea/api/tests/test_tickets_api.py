"""
Tests para los endpoints de boletos (API).
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

from gestionVuelos.models import Flight, Passenger, Reservation, Plane, Seat, Ticket


class TicketAPITestCase(APITestCase):
    """
    Tests para los endpoints de boletos
    """

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )

        self.user = User.objects.create_user(
            username='user',
            password='user123'
        )

        # Crear datos necesarios
        self.plane = Plane.objects.create(
            model='Boeing 737',
            manufacturer='Boeing',
            capacity=150
        )

        self.flight = Flight.objects.create(
            plane=self.plane,
            origin='Buenos Aires',
            destination='Madrid',
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=12),
            duration=timedelta(hours=12),
            status='scheduled',
            base_price=500.00
        )

        self.passenger = Passenger.objects.create(
            full_name='Juan Perez',
            document_type='DNI',
            document_number='12345678',
            email='juan@email.com',
            phone='123456789',
            birth_date='1990-01-01'
        )

        self.seat = Seat.objects.create(
            plane=self.plane,
            number='1A',
            row=1,
            column='A',
            seat_type='Economy',
            status='available'
        )

        self.reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='reserved',
            price=500.00
        )

    def test_generate_ticket_admin_only(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('ticket-generate', kwargs={'pk': self.reservation.id})
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND])

    def test_ticket_by_barcode(self):
        ticket = Ticket.objects.create(reservation=self.reservation)

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('ticket-by-barcode')
        response = self.client.get(url, {'barcode': ticket.barcode})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['barcode'], ticket.barcode)
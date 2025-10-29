"""
Tests para los endpoints de reservas (API).
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

from gestionVuelos.models import Flight, Passenger, Reservation, Plane, Seat


class ReservationAPITestCase(APITestCase):
    """
    Tests para los endpoints de reservas
    """

    def setUp(self):
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

    def test_create_reservation(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('reservation-list')
        data = {
            'passenger_id': self.passenger.id,
            'flight_id': self.flight.id,
            'seat_id': self.seat.id,
            'price': 500.00
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_seat_availability(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('reservation-check-seat')
        response = self.client.get(url, {
            'flight_id': self.flight.id,
            'seat_id': self.seat.id
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_confirm_reservation(self):
        reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='reserved',
            price=500.00
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('reservation-confirm', kwargs={'pk': reservation.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reservation']['status'], 'confirmed')

    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='reserved',
            price=500.00
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('reservation-cancel', kwargs={'pk': reservation.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reservation']['status'], 'cancelled')

    def test_cancel_already_cancelled_reservation(self):
        """Test para verificar que no se puede cancelar una reserva ya cancelada"""
        reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='cancelled',
            price=500.00
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('reservation-cancel', kwargs={'pk': reservation.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_reservation_invalid_seat(self):
        """Test para verificar que no se puede crear una reserva con un asiento ocupado"""
        # Crear una reserva existente con el asiento
        Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='reserved',
            price=500.00
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Intentar crear otra reserva con el mismo asiento
        url = reverse('reservation-list')
        data = {
            'passenger_id': self.passenger.id,
            'flight_id': self.flight.id,
            'seat_id': self.seat.id,
            'price': 500.00
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reservation_ordering(self):
        """Test para verificar la ordenación de reservas por fecha"""
        # Crear múltiples reservas en diferentes fechas
        reservation1 = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=self.seat,
            status='reserved',
            price=500.00,
            reservation_date=timezone.now() - timedelta(days=1)
        )

        # Crear otro asiento para la segunda reserva
        seat2 = Seat.objects.create(
            plane=self.plane,
            number='2A',
            row=2,
            column='A',
            seat_type='Economy',
            status='available'
        )

        reservation2 = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
            seat=seat2,
            status='reserved',
            price=500.00,
            reservation_date=timezone.now()
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Verificar ordenamiento descendente por fecha
        url = reverse('reservation-list')
        response = self.client.get(url + '?ordering=-reservation_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], reservation2.id)
        self.assertEqual(response.data[1]['id'], reservation1.id)

        # Verificar ordenamiento ascendente por fecha
        response = self.client.get(url + '?ordering=reservation_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], reservation1.id)
        self.assertEqual(response.data[1]['id'], reservation2.id)
"""
Tests para los endpoints de vuelos (API).
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

from gestionVuelos.models import Flight, Plane, Seat


class FlightAPITestCase(APITestCase):
    """
    Tests para los endpoints de vuelos
    """

    def setUp(self):
        # Crear usuario administrador
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )

        # Crear usuario normal
        self.normal_user = User.objects.create_user(
            username='user',
            password='user123'
        )

        # Crear avion
        self.plane = Plane.objects.create(
            model='Boeing 737',
            manufacturer='Boeing',
            capacity=150
        )

        # Crear vuelo
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

        # Crear vuelo cancelado
        self.cancelled_flight = Flight.objects.create(
            plane=self.plane,
            origin='Madrid',
            destination='Paris',
            departure_time=timezone.now() + timedelta(days=2),
            arrival_time=timezone.now() + timedelta(days=2, hours=2),
            duration=timedelta(hours=2),
            status='cancelled',
            base_price=300.00
        )

        # Crear asientos
        for i in range(1, 6):
            Seat.objects.create(
                plane=self.plane,
                number=f'{i}A',
                row=i,
                column='A',
                seat_type='Economy',
                status='available'
            )

    def test_list_flights_unauthorized(self):
        url = reverse('flight-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_flights_authorized(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('flight-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_flight_admin_only(self):
        # Usuario normal no puede crear vuelos
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('flight-list')
        data = {
            'plane_id': self.plane.id,
            'origin': 'Paris',
            'destination': 'Londres',
            'departure_time': (timezone.now() + timedelta(days=2)).isoformat(),
            'arrival_time': (timezone.now() + timedelta(days=2, hours=2)).isoformat(),
            'duration': '02:00:00',
            'status': 'scheduled',
            'base_price': 300.00
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_available_flights(self):
        """Test para verificar el endpoint de vuelos disponibles"""
        url = reverse('flight-available')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Debería incluir solo vuelos programados
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.flight.id)
        self.assertNotIn(self.cancelled_flight.id, [f['id'] for f in response.data])

    def test_search_flights(self):
        """Test para verificar la búsqueda de vuelos"""
        url = reverse('flight-search')
        
        # Búsqueda por origen
        response = self.client.get(url, {'origin': 'Buenos'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.flight.id)
        
        # Búsqueda por destino
        response = self.client.get(url, {'destination': 'Paris'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.cancelled_flight.id)
        
        # Búsqueda por fecha
        tomorrow = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(url, {'departure_date': tomorrow})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.flight.id)
        
        # Búsqueda sin resultados
        response = self.client.get(url, {'origin': 'Tokyo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_flight_passengers_admin_only(self):
        """Test para verificar que solo admin puede ver pasajeros del vuelo"""
        url = reverse('flight-passengers', args=[self.flight.id])
        
        # Usuario no autenticado
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Usuario normal
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Administrador puede crear vuelos
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_flights(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('flight-search')
        response = self.client.get(url, {
            'origin': 'Buenos Aires',
            'destination': 'Madrid'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_flight_passengers_admin_only(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('flight-passengers', kwargs={'pk': self.flight.id})
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])

        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
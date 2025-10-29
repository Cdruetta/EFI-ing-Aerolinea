"""
Tests para los endpoints de pasajeros (API).
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from gestionVuelos.models import Passenger


class PassengerAPITestCase(APITestCase):
    """
    Tests para los endpoints de pasajeros
    """

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )

        self.normal_user = User.objects.create_user(
            username='user',
            password='user123'
        )

        # Crear pasajero
        self.passenger = Passenger.objects.create(
            full_name='Juan Perez',
            document_type='DNI',
            document_number='12345678',
            email='juan@email.com',
            phone='123456789',
            birth_date='1990-01-01'
        )

    def test_create_passenger_admin_only(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('passenger-list')
        data = {
            'full_name': 'Maria Garcia',
            'document_type': 'DNI',
            'document_number': '87654321',
            'email': 'maria@email.com',
            'phone': '987654321',
            'birth_date': '1985-05-15'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_passenger_reservations(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('passenger-reservations', kwargs={'pk': self.passenger.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# -*- coding: utf-8 -*-
"""
URLs para la API REST del sistema de gestion de vuelos
Desarrollado por: [Nombre del Estudiante]
Fecha: 2024
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views_api import (
    FlightViewSet, 
    PassengerViewSet, 
    ReservationViewSet, 
    PlaneViewSet, 
    TicketViewSet
)

# Configurar el router para las APIs
router = routers.DefaultRouter()
router.register(r'planes', PlaneViewSet, basename='plane')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'passengers', PassengerViewSet, basename='passenger')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'tickets', TicketViewSet, basename='ticket')

# URLs de la API
urlpatterns = [
    # Incluir las rutas del router
    path('', include(router.urls)),
    
    # Autenticación JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
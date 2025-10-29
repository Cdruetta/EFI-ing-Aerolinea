# -*- coding: utf-8 -*-
"""
URLs de la API REST (app `api`).
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    FlightViewSet,
    PassengerViewSet,
    ReservationViewSet,
    PlaneViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register(r'planes', PlaneViewSet, basename='plane')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'passengers', PassengerViewSet, basename='passenger')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



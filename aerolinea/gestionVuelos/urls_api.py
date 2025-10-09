from django.urls import path, include
from rest_framework import routers
from .views_api import FlightViewSet, PassengerViewSet, ReservationViewSet, PlaneViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register(r'planes', PlaneViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

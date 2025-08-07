from django.urls import path
from .views import (
    HomeView,

    # Vuelos
    FlightListView, 
    FlightDetailView, 
    FlightCreateView, 
    FlightUpdateView, 
    FlightDeleteView,

    # Pasajeros
    PassengerListView, 
    PassengerDetailView, 
    PassengerCreateView, 
    PassengerUpdateView, 
    PassengerDeleteView,

    # Aviones
    PlaneListView,
    PlaneCreateView,
    PlaneUpdateView,
    PlaneDeleteView,
    PlaneDetailView,


    # Reservas
    ReservationCreateView,  
)

from home.views import LoginView, LogoutView, RegisterView

app_name = "gestionVuelos"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Rutas para vuelos
    path("flights/", FlightListView.as_view(), name="flight_list"),
    path("flights/create/", FlightCreateView.as_view(), name="flight_create"),
    path("flights/<int:pk>/", FlightDetailView.as_view(), name="flight_detail"),
    path("flights/<int:pk>/edit/", FlightUpdateView.as_view(), name="flight_edit"),
    path("flights/<int:pk>/delete/", FlightDeleteView.as_view(), name="flight_delete"),

    # Rutas para pasajeros
    path("passengers/", PassengerListView.as_view(), name="passenger_list"),
    path("passengers/create/", PassengerCreateView.as_view(), name="passenger_create"),
    path("passengers/<int:pk>/", PassengerDetailView.as_view(), name="passenger_detail"),
    path("passengers/<int:pk>/edit/", PassengerUpdateView.as_view(), name="passenger_edit"),
    path("passengers/<int:pk>/delete/", PassengerDeleteView.as_view(), name="passenger_delete"),

    # Rutas para aviones
    path("planes/", PlaneListView.as_view(), name="plane_list"),
    path("planes/create/", PlaneCreateView.as_view(), name="plane_create"), 
    path("planes/<int:pk>/edit/", PlaneUpdateView.as_view(), name="plane_edit"),
    path("planes/<int:pk>/delete/", PlaneDeleteView.as_view(), name="plane_delete"),

    # Rutas para planes (planes tarifarios)
    path("plans/", PlaneListView.as_view(), name="plan_list"),
    path("plane/create/", PlaneCreateView.as_view(), name="plan_create"),
    path("plans/<int:pk>/", PlaneDetailView.as_view(), name="plan_detail"),
    path("plans/<int:pk>/edit/", PlaneUpdateView.as_view(), name="plan_edit"),
    path("plans/<int:pk>/delete/", PlaneDeleteView.as_view(), name="plan_delete"),

    # Rutas para reservas
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation_create"),

    # Rutas de autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
]

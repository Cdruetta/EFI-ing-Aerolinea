from django.urls import path
from .views import (
    HomeView,
    FlightListView, 
    FlightDetailView, 
    FlightCreateView, 
    FlightUpdateView, 
    FlightDeleteView,
    PassengerListView, 
    PassengerDetailView, 
    PassengerCreateView, 
    PassengerUpdateView, 
    PassengerDeleteView,
    PlaneListView,
    ReservationCreateView,  
)
from home.views import LoginView, LogoutView, RegisterView

app_name = "gestionVuelos"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Vuelos
    path("flights/", FlightListView.as_view(), name="flight_list"),
    path("flights/create/", FlightCreateView.as_view(), name="flight_create"),
    path("flights/<int:pk>/", FlightDetailView.as_view(), name="flight_detail"),
    path("flights/<int:pk>/edit/", FlightUpdateView.as_view(), name="flight_edit"),
    path("flights/<int:pk>/delete/", FlightDeleteView.as_view(), name="flight_delete"),

    # Pasajeros
    path("passengers/", PassengerListView.as_view(), name="passenger_list"),
    path("passengers/create/", PassengerCreateView.as_view(), name="passenger_create"),
    path("passengers/<int:pk>/", PassengerDetailView.as_view(), name="passenger_detail"),
    path("passengers/<int:pk>/edit/", PassengerUpdateView.as_view(), name="passenger_edit"),
    path("passengers/<int:pk>/delete/", PassengerDeleteView.as_view(), name="passenger_delete"),

    # Aviones
    path("planes/", PlaneListView.as_view(), name="plane_list"),

    # Reservas - agregar ruta para crear reserva
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation_create"),

    # Rutas para autenticación usando vistas de home
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
]

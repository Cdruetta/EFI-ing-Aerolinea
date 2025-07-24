from django.urls import path
from .views import (
    home_view,
    plane_list,
    passenger_list,
    flight_list,
    flight_detail,
    flight_edit,
    flight_delete,
    flight_create,
    passenger_create,
    passenger_detail,
    passenger_edit,
    passenger_delete,
)

urlpatterns = [
    path(route="", view=home_view, name="home"),
    path(route="flights/", view=flight_list, name="flight_list"),
    path(route="flights/<int:pk>/", view=flight_detail, name="flight_detail"),
    path(route="flights/<int:pk>/edit/", view=flight_edit, name="flight_edit"),
    path(route="flights/<int:pk>/delete/", view=flight_delete, name="flight_delete"),
    path(route="flights/create/", view=flight_create, name="flight_create"),
    # Primero las rutas más específicas para passengers:
    path(route="passenger/create/", view=passenger_create, name="passenger_create"),
    path(route="passenger/<int:pk>/edit/", view=passenger_edit, name="passenger_edit"),
    path(
        route="passenger/<int:pk>/delete/",
        view=passenger_delete,
        name="passenger_delete",
    ),
    path(route="passenger/<int:pk>/", view=passenger_detail, name="passenger_detail"),
    # Luego la ruta general de lista
    path(route="passenger/", view=passenger_list, name="passenger_list"),
    path(route="planes/", view=plane_list, name="plane_list"),
]

from django.urls import path

from gestionVuelos.views import plane_list, passenger_list, flight_list

urlpatterns = [
    path(
        route='planes/', 
        view=plane_list, 
        name='planes'
    ),
    path(
        route='passenger/', 
        view=passenger_list, 
        name='passenger'
    ),
    path(
        route='flights/', 
        view=flight_list, 
        name='flights'
    ),
]

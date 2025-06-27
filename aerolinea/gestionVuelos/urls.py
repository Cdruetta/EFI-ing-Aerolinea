from django.urls import path

from gestionVuelos.views import plane_list, passenger_list

urlpatterns = [
    path(
        route='planes_list/', 
        view=plane_list, 
        name='planes'
    ),
    path(
        route='passenger_list/', 
        view=passenger_list, 
        name='passenger'
    ),
]

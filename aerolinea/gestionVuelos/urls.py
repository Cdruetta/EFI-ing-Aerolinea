from django.urls import path
from .views import (
    home_view,
    plane_list,
    passenger_list,
    flight_list,
    flight_detail,
    flight_edit,
    flight_delete
)

app_name = 'gestionVuelos'

urlpatterns = [
    path(
        route='', 
        view=home_view, 
        name='home'
        ),
    path(
        route='home/', 
        view=home_view, 
        name='home_page'
        ),
    path(
        route='planes/', 
        view=plane_list, 
        name='plane_list'
        ),
    path(
        route='passenger/', 
        view=passenger_list, 
        name='passenger_list'
        ),
    path(
        route='flights/', 
        view=flight_list, 
        name='flight_list'
        ),
    path(
        route='flights/<int:pk>/', 
        view=flight_detail, 
        name='flight_detail'
        ),
    path(
        route='flights/<int:pk>/edit/', 
        view=flight_edit, 
        name='flight_edit'
        ),
    path(
        route='flights/<int:pk>/delete/', 
        view=flight_delete, 
        name='flight_delete'
        ),
]

    



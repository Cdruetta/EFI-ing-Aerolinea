from django.urls import path
from .views import home_view, plane_list, passenger_list, flight_list

urlpatterns = [
    path('', home_view, name='home'),                # /gestionVuelos/
    path('home/', home_view, name='home_page'),      # /gestionVuelos/home/
    path('planes/', plane_list, name='plane_list'),
    path('passenger/', passenger_list, name='passenger_list'),
    path('flights/', flight_list, name='flight_list'),
]



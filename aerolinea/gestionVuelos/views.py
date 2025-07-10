from django.shortcuts import render

from gestionVuelos.services.plane import PlaneService
from gestionVuelos.services.flights import FlightService
from gestionVuelos.services.passenger import PassengerService


# Create your views here.
from django.shortcuts import render

def home_view(request):
    return render(request, 'gestionVuelos/home.html')



def plane_list(request):
    all_planes = PlaneService.get_all()
    return render(
        request, 
        'planes/list.html'
        ,{
            'planes': all_planes,
            'otro_atributo': 'Atributo 2'
        }
        
        )

def passenger_list(request):
    all_passengers = PassengerService.get_all()
    return render(
        request,
        'passenger/list.html',
        {
            'passengers': all_passengers,
            'titulo': 'Lista de Pasajeros'
        }
    )


def flight_list(request):
    all_flights = FlightService.get_all()
    return render(
        request,
        'flights/list.html',
        {
            'flights': all_flights,
            'titulo': 'Lista de Vuelos'
        }
    )

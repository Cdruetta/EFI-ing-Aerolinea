from django.shortcuts import render, get_object_or_404

from gestionVuelos.services.plane import PlaneService
from gestionVuelos.services.flights import FlightService
from gestionVuelos.services.passenger import PassengerService
from gestionVuelos.models import Flight


# Create your views here.
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')



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

def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    passenger_id = request.GET.get('passenger_id')  # Recibimos por query param (opcional)
    return render(request, 'flights/detail.html', {'flight': flight, 'passenger_id': passenger_id})

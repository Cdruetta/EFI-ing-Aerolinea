from django.shortcuts import render, get_object_or_404, redirect

from gestionVuelos.services.plane import PlaneService
from gestionVuelos.services.flights import FlightService
from gestionVuelos.services.passenger import PassengerService
from gestionVuelos.models import Flight
from gestionVuelos.forms import FlightForm


# Create your views here.
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def plane_list(request):
    all_planes = PlaneService.get_all()
    return render(
        request, 
        'planes/list.html',
        dict(
            planes=all_planes,
            otro_atributo='Atributo 2'
        )
    )

def passenger_list(request):
    all_passengers = PassengerService.get_all()
    return render(
        request,
        'passenger/list.html',
        dict(
            passengers=all_passengers,
            titulo='Lista de Pasajeros'
        )
    )

def flight_list(request):
    all_flights = FlightService.get_all()
    return render(
        request,
        'flights/list.html',
        dict(
            flights=all_flights,
            titulo='Lista de Vuelos'
        )
    )

def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    passenger_id = request.GET.get('passenger_id')
    return render(
        request,
        'flights/detail.html',
        dict(
            flight=flight,
            passenger_id=passenger_id
        )
    )

def flight_edit(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('flight_detail', pk=pk)
    else:
        form = FlightForm(instance=flight)

    return render(
        request,
        'flights/edit.html',
        dict(
            form=form,
            flight=flight,
            titulo='Editar Vuelo'
        )
    )
def flight_delete(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    flight.delete()
    return redirect('flight_list')


from django.shortcuts import render, get_object_or_404, redirect

from gestionVuelos.models import Passenger, Flight
from gestionVuelos.forms import FlightForm, PassengerForm
from gestionVuelos.services.plane import PlaneService
from gestionVuelos.services.flights import FlightService
from gestionVuelos.services.passenger import PassengerService


def home_view(request):
    return render(request, "home.html")


def plane_list(request):
    all_planes = PlaneService.get_all()
    return render(
        request, "planes/list.html", dict(planes=all_planes, otro_atributo="Atributo 2")
    )


def passenger_list(request):
    all_passengers = PassengerService.get_all()
    return render(
        request,
        "passenger/list.html",
        dict(passengers=all_passengers, titulo="Lista de Pasajeros"),
    )


def passenger_detail(request, pk):
    passenger = PassengerService.get_by_id(pk)
    passenger = get_object_or_404(Passenger, pk=pk) if passenger is None else passenger
    return render(request, "passenger/detail.html", dict(passenger=passenger))


def passenger_create(request):
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestionVuelos:passenger_list")
    else:
        form = PassengerForm()
    return render(request, "passenger/create.html", dict(form=form))


def passenger_edit(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    if request.method == "POST":
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return redirect("gestionVuelos:passenger_detail", pk=pk)
    else:
        form = PassengerForm(instance=passenger)
    return render(request, "passenger/edit.html", dict(form=form, passenger=passenger))


def passenger_delete(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    if request.method == "POST":
        passenger.delete()
        return redirect("gestionVuelos:passenger_list")
    return render(request, "passenger/delete_confirm.html", dict(passenger=passenger))


def flight_list(request):
    all_flights = FlightService.get_all()
    return render(
        request,
        "flights/list.html",
        dict(flights=all_flights, titulo="Lista de Vuelos"),
    )


def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    passenger_id = request.GET.get("passenger_id")
    return render(
        request, "flights/detail.html", dict(flight=flight, passenger_id=passenger_id)
    )


def flight_edit(request, pk):
    flight = get_object_or_404(Flight, pk=pk)

    if request.method == "POST":
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect("gestionVuelos:flight_detail", pk=pk)
    else:
        form = FlightForm(instance=flight)
    return render(
        request,
        "flights/edit.html",
        dict(form=form, flight=flight, titulo="Editar Vuelo"),
    )


def flight_create(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestionVuelos:flight_list")
    else:
        form = FlightForm()
    return render(request, "flights/create.html", dict(form=form))


def flight_delete(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == "POST":
        flight.delete()
        return redirect("gestionVuelos:flight_list")
    return render(request, "flights/delete_confirm.html", dict(flight=flight))

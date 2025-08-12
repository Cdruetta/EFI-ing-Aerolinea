from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, ListView
from django.db.models import Q

from gestionVuelos.models import Passenger, Flight, Plane, Reservation, Seat, Reservation
from gestionVuelos.forms import FlightForm, PassengerForm, PlaneForm

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin para restringir acceso a staff o superusuarios"""
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

class HomeView(TemplateView):
    template_name = "home.html"

# --- Pasajeros ---
class PassengerListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Passenger
    template_name = "passenger/list.html"
    context_object_name = "passengers"
    login_url = '/login/'

class PassengerDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Passenger
    template_name = "passenger/detail.html"
    context_object_name = "passenger"
    login_url = '/login/'

class PassengerCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "passenger/create.html"
    success_url = reverse_lazy("gestionVuelos:passenger_list")
    login_url = '/login/'

class PassengerUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "passenger/edit.html"
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy("gestionVuelos:passenger_detail", kwargs={"pk": self.object.pk})

class PassengerDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Passenger
    template_name = "passenger/delete_confirm.html"
    success_url = reverse_lazy("gestionVuelos:passenger_list")
    login_url = '/login/'

# --- Vuelos ---
class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = "flights/list.html"
    context_object_name = "flights"
    login_url = '/login/'
    paginate_by = 10

class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = "flights/detail.html"
    context_object_name = "flight"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_seats = self.get_object().get_available_seats()
        context["available_seats"] = available_seats
        
        if not available_seats.exists():
            context['mensaje'] = "No hay asientos disponibles para este vuelo."
        else:
            context['mensaje'] = f"Hay {available_seats.count()} asientos disponibles."
        
        return context

class FlightCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Flight
    form_class = FlightForm
    template_name = "flights/create.html"
    success_url = reverse_lazy("gestionVuelos:flight_list")
    login_url = '/login/'

class FlightUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = "flights/edit.html"
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy("gestionVuelos:flight_detail", kwargs={"pk": self.object.pk})

class FlightDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Flight
    template_name = "flights/delete_confirm.html"
    success_url = reverse_lazy("gestionVuelos:flight_list")
    login_url = '/login/'

# --- Planes ---
class PlaneListView(StaffRequiredMixin, LoginRequiredMixin, ListView):
    model = Plane
    template_name = "planes/list.html"
    context_object_name = "planes"
    login_url = '/login/'

class PlaneDetailView(StaffRequiredMixin, LoginRequiredMixin, DetailView):
    model = Plane
    template_name = "planes/detail.html"
    context_object_name = "plane"
    login_url = '/login/'

class PlaneCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Plane
    form_class = PlaneForm
    template_name = "planes/plane_form.html"
    success_url = reverse_lazy("gestionVuelos:plane_list")
    login_url = '/login/'

class PlaneUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Plane
    form_class = PlaneForm
    template_name = "planes/plane_form.html"
    success_url = reverse_lazy("gestionVuelos:plane_list")
    login_url = '/login/'

class PlaneDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Plane
    template_name = "planes/plane_confirm_delete.html"
    success_url = reverse_lazy("gestionVuelos:plane_list")
    login_url = '/login/'

# --- Reservas ---
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = []  # No usamos fields porque manejamos el asiento manualmente
    template_name = "reservations/create.html"
    login_url = '/login/'

    def get_success_url(self):
        # Usamos self.reservation que guardamos en post()
        return reverse_lazy("gestionVuelos:reservation_detail", kwargs={"pk": self.reservation.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = get_object_or_404(Flight, pk=self.kwargs['flight_id'])
        
        available_seats = Seat.objects.filter(
            plane=flight.plane,
            status="available"
        ).order_by('row', 'column')

        seat_rows = {}
        for seat in available_seats:
            seat_rows.setdefault(seat.row, []).append(seat)
        
        context['flight'] = flight
        context['seat_rows'] = seat_rows
        context['seat_types'] = dict(Seat.SEAT_STATUS_CHOICES) if hasattr(Seat, 'SEAT_STATUS_CHOICES') else {}

        return context

    def post(self, request, *args, **kwargs):
        flight = get_object_or_404(Flight, pk=self.kwargs['flight_id'])
        passenger = get_object_or_404(Passenger, user=self.request.user)
        seat_id = request.POST.get('seat')

        if not seat_id:
            messages.error(request, "Debe seleccionar un asiento")
            return redirect(self.request.path)

        try:
            seat = Seat.objects.get(
                pk=seat_id,
                plane=flight.plane,
                status="available"
            )
        except Seat.DoesNotExist:
            messages.error(request, "El asiento seleccionado no está disponible")
            return redirect(self.request.path)

        try:
            self.reservation = Reservation.objects.create(
                flight=flight,
                passenger=passenger,
                seat=seat,
                status='reserved',
                price=flight.base_price,
            )
        except Exception as e:
            messages.error(request, f"No se pudo crear la reserva: {e}")
            return redirect(self.request.path)

        seat.status = "reserved"
        seat.save()

        messages.success(request, "Reserva realizada con éxito!")
        return redirect(self.get_success_url())



class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservations/detail.html"
    context_object_name = "reservation"
    login_url = '/login/'

class MyReservationsListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservations/my_reservations.html"
    context_object_name = "reservations"
    login_url = '/login/'

    def get_queryset(self):
        
        return Reservation.objects.filter(passenger__user=self.request.user, status='reserved')
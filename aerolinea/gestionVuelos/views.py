from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from gestionVuelos.models import Passenger, Flight, Plane, Reservation
from gestionVuelos.forms import FlightForm, PassengerForm

# Mixin para restringir acceso a staff o superusuario
class StaffRequiredMixin(UserPassesTestMixin):
    raise_exception = True  # Lanza PermissionDenied en vez de redirigir

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)

class HomeView(TemplateView):
    template_name = "home.html"


# --- Pasajeros ---
class PassengerListView(LoginRequiredMixin, ListView):
    model = Passenger
    template_name = "passenger/list.html"
    context_object_name = "passengers"
    login_url = '/login/'

class PassengerDetailView(LoginRequiredMixin, DetailView):
    model = Passenger
    template_name = "passenger/detail.html"
    context_object_name = "passenger"
    login_url = '/login/'

class PassengerCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "passenger/create.html"
    success_url = reverse_lazy("gestionVuelos:passenger_list")
    login_url = '/login/'

class PassengerUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
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

class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = "flights/detail.html"
    context_object_name = "flight"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passenger_id"] = self.request.GET.get("passenger_id")
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


# --- Aviones ---
class PlaneListView(LoginRequiredMixin, ListView):
    model = Plane
    template_name = "planes/list.html"
    context_object_name = "planes"
    login_url = '/login/'


# --- Reservas (para que pasajero pueda reservar un vuelo) ---
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['flight', 'seat']
    template_name = "reservations/create.html"
    success_url = reverse_lazy("gestionVuelos:flight_list")
    login_url = '/login/'

    def form_valid(self, form):
        try:
            passenger = Passenger.objects.get(user=self.request.user)
        except Passenger.DoesNotExist:
            # Redirigir a crear pasajero si no existe
            return redirect('gestionVuelos:passenger_create')

        # Asignar pasajero y estado
        form.instance.passenger = passenger
        form.instance.status = 'reserved'

        # Validar que el asiento pertenezca al avión del vuelo
        if form.instance.seat.plane != form.instance.flight.plane:
            form.add_error('seat', 'El asiento no pertenece al avión del vuelo.')
            return self.form_invalid(form)

        return super().form_valid(form)
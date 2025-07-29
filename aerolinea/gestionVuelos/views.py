from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from gestionVuelos.models import Passenger, Flight, Plane
from gestionVuelos.forms import FlightForm, PassengerForm


class HomeView(TemplateView):
    template_name = "home.html"


class PassengerListView(ListView):
    model = Passenger
    template_name = "passenger/list.html"
    context_object_name = "passengers"


class PassengerDetailView(DetailView):
    model = Passenger
    template_name = "passenger/detail.html"
    context_object_name = "passenger"


class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "passenger/create.html"
    success_url = reverse_lazy("gestionVuelos:passenger_list")


class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "passenger/edit.html"

    def get_success_url(self):
        return reverse_lazy("gestionVuelos:passenger_detail", kwargs={"pk": self.object.pk})


class PassengerDeleteView(DeleteView):
    model = Passenger
    template_name = "passenger/delete_confirm.html"
    success_url = reverse_lazy("gestionVuelos:passenger_list")


class FlightListView(ListView):
    model = Flight
    template_name = "flights/list.html"
    context_object_name = "flights"


class FlightDetailView(DetailView):
    model = Flight
    template_name = "flights/detail.html"
    context_object_name = "flight"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passenger_id"] = self.request.GET.get("passenger_id")
        return context


class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = "flights/create.html"
    success_url = reverse_lazy("gestionVuelos:flight_list")


class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = "flights/edit.html"

    def get_success_url(self):
        return reverse_lazy("gestionVuelos:flight_detail", kwargs={"pk": self.object.pk})


class FlightDeleteView(DeleteView):
    model = Flight
    template_name = "flights/delete_confirm.html"
    success_url = reverse_lazy("gestionVuelos:flight_list")


class PlaneListView(ListView):
    model = Plane
    template_name = "planes/list.html"
    context_object_name = "planes"

from django import forms
from .models import Flight
from gestionVuelos.models import Passenger


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            "plane",
            "origin",
            "destination",
            "departure_time",
            "arrival_time",
            "duration",
            "status",
            "base_price",
        ]
        widgets = {
            "plane": forms.Select(attrs={"class": "form-select"}),
            "origin": forms.TextInput(attrs={"class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "departure_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "arrival_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "duration": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "hh:mm:ss"}
            ),
            "status": forms.TextInput(attrs={"class": "form-control"}),
            "base_price": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            "full_name",
            "document_type",
            "document_number",
            "email",
            "phone",
            "birth_date",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "document_type": forms.Select(attrs={"class": "form-select"}),
            "document_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

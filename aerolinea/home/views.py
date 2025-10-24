from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.utils.translation import gettext as _
from gestionVuelos.models import Passenger

from home.forms import LoginForm, RegisterForm

import logging

logger = logging.getLogger(__name__)

class HomeView(View):
    def get(self, request):
        logger.error("Ingresando a view")
        return render(request, "index.html")

    def post(self, request):

        return render(request, "index.html")


def _validate_pass(pass1, pass2):

    print(pass1 == pass2)
    pass1 == pass2


class LoginView(View):
    def get(self, request):
        logger.error("Login user")
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Sesión iniciada")
                return redirect("index")
            else:
                messages.error(request, "El usuario o contraseña no coinciden")
        return render(request, "accounts/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Sesión cerrada")
        return redirect("login")


class RegisterView(View):
    def get(self, request):
        logger.error("Registro user")
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                email=form.cleaned_data["email"],
            )
            
            # Actualizar el pasajero creado por la señal con los datos reales
            try:
                passenger = Passenger.objects.get(user=user)
                passenger.document_number = form.cleaned_data["document_number"]
                passenger.full_name = form.cleaned_data["username"]
                passenger.email = form.cleaned_data["email"]
                passenger.save()
            except Passenger.DoesNotExist:
                # Si por alguna razón no existe el pasajero, crearlo manualmente
                Passenger.objects.create(
                    user=user,
                    full_name=form.cleaned_data["username"],
                    document_number=form.cleaned_data["document_number"],
                    email=form.cleaned_data["email"],
                    phone='',
                    birth_date='1900-01-01',
                    document_type=Passenger.DNI
                )
            
            messages.success(request, "Usuario creado correctamente.")
            return redirect("login")

        return render(request, "accounts/register.html", {"form": form})

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.utils.translation import gettext as _


from home.forms import LoginForm, RegisterForm


class HomeView(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        return render(request, "index.html")


def _validate_pass(pass1, pass2):

    print(pass1 == pass2)
    pass1 == pass2


class LoginView(View):
    def get(self, request):
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
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                email=form.cleaned_data["email"],
            )
            messages.success(request, "Usuario creado correctamente.")
            return redirect("login")

        return render(request, "accounts/register.html", {"form": form})

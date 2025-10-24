from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from gestionVuelos.models import Passenger  # Asegurate de importar Passenger

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese nombre de usuario",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )
    
    password = forms.CharField(
        max_length=128,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese contraseña",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese nombre de usuario",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=128,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese contraseña",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

    password2 = forms.CharField(
        max_length=128,
        label="Repita el password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Repita el password",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese correo electrónico",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

    document_number = forms.CharField(
        max_length=20,
        label="Número de documento",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-60 personalizado",
                "placeholder": "Ingrese su número de documento",
                "style": "background-color: #f0f0f0;",
            }
        ),
    )

    # VALIDACIONES
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está en uso.")
        return email

    def clean_document_number(self):
        document_number = self.cleaned_data.get("document_number")
        if Passenger.objects.filter(document_number=document_number).exists():
            raise ValidationError("Este número de documento ya está registrado.")
        return document_number

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

"""
URL configuration for aerolinea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from gestionVuelos.views import FlightCreateView
from home.views import RegisterView, LogoutView

def prueba_sentry(request):
    sentry_sdk.capture_message("✅ Sentry funcionando en Django")
    return HttpResponse("Mensaje enviado a Sentry")

urlpatterns = [
    path('', lambda request: redirect('gestionVuelos:home'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('gestionVuelos/', include(('gestionVuelos.urls', 'gestionVuelos'), namespace='gestionVuelos')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
    
]




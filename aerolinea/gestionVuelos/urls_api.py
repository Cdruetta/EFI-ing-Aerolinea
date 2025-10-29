"""
Wrappers para compatibilidad: redirige a `api.urls` sin cambiar rutas existentes.
"""

from django.urls import include, path

urlpatterns = [
    path('', include('api.urls')),
]
from django.shortcuts import render

from gestionVuelos.services.plane import PlaneService


# Create your views here.

def plane_list(request):
    all_planes = PlaneService.get_all()
    return render(
        request, 
        'planes/list.html'
        ,{
            'planes': all_planes,
            'otro_atributo': 'Atributo 2'
        }
        
        )

def passenger_list(request):
    return render(request, 'passenger/list.html')

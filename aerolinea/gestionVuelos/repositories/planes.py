from django.shortcuts import get_object_or_404

from gestionVuelos.models import Plane
from typing import List
from typing import Optional


class PlaneRepository:

    @staticmethod
    def get_all() -> list[Plane]: 
        return list(Plane.objects.all())
    
    @staticmethod
    def get_by_id(plane_id: int) -> Optional[Plane]:
        try:
            return Plane.objects.get(id=plane_id)
        except Plane.DoesNotExist:
            return None
    
    @staticmethod
    def search_by_name(name: str) -> List[Plane]:
        return list(Plane.objects.filter(model__icontains=name))
    
    @staticmethod
    def create(
        model: str, 
        capacity: int, 
        available_seats: int,
    ) -> Plane:
        return Plane.objects.create(
            model=model,
            capacity=capacity,
            available_seats=available_seats
        )
        
    
    @staticmethod
    def delete(plane_id: int) -> None:
        try:
            Plane.objects.get(id=plane_id).delete()
        except Plane.DoesNotExist:
            raise ValueError("Plane does not exist") 
        

    @staticmethod
    def update(plane: Plane, model: str, capacity: int) -> Plane:
        plane.model = model
        plane.capacity = capacity
        plane.save()
        return plane


    

            

        
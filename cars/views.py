from django.shortcuts import render
from rest_framework import viewsets
from .serializer import CarSerializer,BrandSerializer
from .models import Car,Brand

#vista basica para las tareas
# Create your views here.
class CarsView(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    
class BrandsView(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
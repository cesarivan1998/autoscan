from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

class Car(models.Model):
    
    FUEL = [
        ('diesel', 'Diesel'),
        ('gasolina', 'Gasolina'),
    ]
    license_plate = models.CharField(primary_key=True, max_length=10)
    fuel_type = models.CharField(max_length=10, choices=FUEL, default='Gasolina')
    tank_capacity = models.PositiveIntegerField()
    horse_power = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', verbose_name='Marca',null=True)
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images/brands/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"

class Car(models.Model):
    
    FUEL = [
        ('diesel', 'Diesel'),
        ('gasolina', 'Gasolina'),
    ]
    license_plate = models.CharField(primary_key=True, max_length=10)
    model = models.CharField(max_length=100, null=True)
    fuel_type = models.CharField(max_length=10, choices=FUEL, default='Gasolina')
    tank_capacity = models.PositiveIntegerField()
    horse_power = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    car_image = models.ImageField(upload_to='images/cars/', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', verbose_name='Marca',null=True)
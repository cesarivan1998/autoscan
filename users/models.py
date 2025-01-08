# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from cars.models import Car
import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    pattern = r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    if not re.match(pattern, value):
        raise ValidationError(f"El número de teléfono {value} no es válido.")

def validate_email(value):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, value):
        raise ValidationError(f"El correo electrónico {value} no es válido.")

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=9, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car, related_name="wishlisted_by")

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    def __str__(self):
        return {self.user.full_name}


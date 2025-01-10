from django.contrib import admin
from .models import Car, Brand

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','logo')
    list_filter = ('name',)

admin.site.register(Brand, BrandAdmin)

class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'fuel_type', 'tank_capacity', 'horse_power', 'year', 'brand')
    list_filter = ('brand',)

admin.site.register(Car, CarAdmin)
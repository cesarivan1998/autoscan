from rest_framework import serializers
from .models import Car,Brand


#convertir datos en formato python a json
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        # fields = ('id','title','description','done')
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        # fields = ('id','title','description','done')
        fields = '__all__'
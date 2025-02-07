from rest_framework import serializers
from apps.locations.models import Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    class Meta:
        model = City
        fields = ['id', 'name', 'province',]
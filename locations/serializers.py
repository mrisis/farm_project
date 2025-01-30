from rest_framework import serializers
from .models import Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(),source='province', write_only=True)
    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'province_id']
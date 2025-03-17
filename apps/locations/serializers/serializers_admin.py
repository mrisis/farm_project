from apps.locations.models import Province, City
from rest_framework import serializers


class ProvinceListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "code"]



class ProvinceDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "code"]




class ProvinceCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "code"]


class ProvinceUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "code"]



class CityListAdminSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(source="province.name")
    class Meta:
        model = City
        fields = ["id", "name", "province"]



class CityDetailAdminSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(source="province.name")
    class Meta:
        model = City
        fields = ["id", "name", "province"]


class CityCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "province"]


class CityUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "province"]










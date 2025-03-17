from apps.locations.models import Province, City
from rest_framework import serializers


class ProvinceListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "code"]



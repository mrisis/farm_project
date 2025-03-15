from apps.accounts.models import User
from rest_framework import serializers



class AdminLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField()






        
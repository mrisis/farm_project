from rest_framework import serializers
from .models import OtpCode, User

class SendOtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['mobile_number',]


class VerifyOtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['mobile_number', 'otp_code',]


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile_number',]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'mobile_number', 'email','gender', 'is_active', 'created_at', 'updated_at',]


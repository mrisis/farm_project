from rest_framework import serializers
from apps.accounts.models import OtpCode, User, RoleCategory, Role


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
        fields = ['mobile_number', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'last_name': {'required': True, 'allow_null': False, 'allow_blank': False},
        }


class RoleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id','name', 'description',]


class RoleSerializer(serializers.ModelSerializer):
    category = RoleCategorySerializer(read_only=True)
    class Meta:
        model = Role
        fields = ['id','name', 'description', 'category',]
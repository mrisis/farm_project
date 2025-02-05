from rest_framework import serializers
from .models import OtpCode, User, RoleCategory, Role

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




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'mobile_number', 'email','gender', 'is_active', 'created_at', 'updated_at',]


class RoleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id','name', 'description',]

class RoleSerializer(serializers.ModelSerializer):
    category = RoleCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=RoleCategory.objects.all(), source='category', write_only=True)
    class Meta:
        model = Role
        fields = ['id','name', 'description', 'category', 'category_id',]
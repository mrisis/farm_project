from rest_framework import serializers
from apps.accounts.models import OtpCode, User, RoleCategory, Role, UserAddress, UserRole
from apps.locations.serializers.serializers_user import ProvinceSerializer, CitySerializer


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


class UserAddressListSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ['id', 'province', 'city', 'full_address', 'postal_code', 'lat', 'lng',]

class RoleNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name',
                  ]
class UserRolesListSerializer(serializers.ModelSerializer):
    role = RoleNestedSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'role',]
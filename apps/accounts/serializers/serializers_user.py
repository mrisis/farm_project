from rest_framework import serializers
from apps.accounts.models import OtpCode, User, RoleCategory, Role, UserAddress, UserRole


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
    province = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = UserAddress
        fields = ['id', 'province', 'city', 'full_address', 'postal_code', 'lat', 'lng',]

    def get_province(self, obj):
        return {

            'id': obj.province.id,
            'name': obj.province.name,
        }

    def get_city(self, obj):
        return {
            'id': obj.city.id,
            'name': obj.city.name,
        }


class UserAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['province', 'city', 'full_address', 'postal_code', 'lat', 'lng',]

class RoleNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name',]


class UserRolesListSerializer(serializers.ModelSerializer):
    role = RoleNestedSerializer(read_only=True)
    role_icon = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ['id', 'role', 'role_icon']

    def get_role_icon(self, obj):
        return obj.role.icon.url if obj.role.icon else None

class UserRoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role',]

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'mobile_number', 'gender', 'profile_image',]

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        data['profile_image'] = None
        if instance.profile_image is not None:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.image.url)

        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image']


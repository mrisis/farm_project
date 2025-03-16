from apps.accounts.models import User, RoleCategory, Role
from rest_framework import serializers
from apps.locations.models import Province
from apps.accounts.models import UserAddress
from apps.accounts.mixins import ImageUrlMixin
class AdminLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField()




class UserListAdminSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_image', 'mobile_number', 'province']

    def get_province(self, obj):
        user_address = UserAddress.objects.filter(user=obj).first()
        if user_address:
            return user_address.province.name
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_image'] = None
        if instance.profile_image:
            data['profile_image'] = self.context['request'].build_absolute_uri(instance.profile_image.image.url)
        return data




class UserDetailAdminSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_image', 'mobile_number', 'roles', 'addresses']

    
    def get_roles(self, obj):
        roles = obj.user_roles.all()
        return [
            {
                'id': role.role.id,
                'name': role.role.name,
            } for role in roles]
    

    def get_addresses(self, obj):
        addresses = obj.addresses.all()

        return [
            {
                'id': address.id,
                'full_address': address.full_address,
                'lat': address.lat,
                'lng': address.lng,
                'province': address.province.name,
                'city': address.city.name
            } for address in addresses]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_image'] = None
        if instance.profile_image:
            data['profile_image'] = self.context['request'].build_absolute_uri(instance.profile_image.image.url)
        return data
    


class UserUpdateAdminSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_number', 'image', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_image'] = None
        if instance.profile_image:
            data['profile_image'] = self.context['request'].build_absolute_uri(instance.profile_image.image.url)
        return data



class UserCreateAdminSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_number', 'image', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password and confirm password do not match'})
        return attrs
    

        
        
        
class RoleCategoryListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id', 'name', 'description',]

    
    def to_representation(self, instance):
         # description is slice to 70 characters
         data = super().to_representation(instance)
         data['description'] = data['description'][:70]
         return data
    

class RoleCategoryDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id', 'name', 'description',]


class RoleCategoryCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id', 'name', 'description',]


class RoleCategoryUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategory
        fields = ['id', 'name', 'description',]



class RoleListAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'category', 'icon']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = self.get_image_url(instance, image_field='icon', default=None)
        data['category'] = instance.category.name
        return data
    


class RoleDetailAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'category', 'icon']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = self.get_image_url(instance, image_field='icon', default=None)
        data['category'] = instance.category.name
        return data


class RoleCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'category', 'icon']


class RoleUpdateAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'category', 'icon']

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = self.get_image_url(instance, image_field='icon', default=None)
        return data

    




    


    



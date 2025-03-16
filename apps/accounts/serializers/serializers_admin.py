from apps.accounts.models import User
from rest_framework import serializers
from apps.locations.models import Province
from apps.accounts.models import UserAddress

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
    

        
        
        
        
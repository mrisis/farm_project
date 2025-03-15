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
            data['profile_image'] = self.context['request'].build_absolute_uri(instance.profile_image.url)
        return data


        
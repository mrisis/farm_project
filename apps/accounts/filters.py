import django_filters
from .models import Role, User, UserAddress

class RoleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['category', 'category_name']



class UserFilterAdmin(django_filters.FilterSet):
    role_name = django_filters.CharFilter(field_name='user_roles__role__name', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['role_name']


class UserAddressFilterAdmin(django_filters.FilterSet):
    user_mobile_number = django_filters.CharFilter(field_name='user__mobile_number', lookup_expr='icontains')
    province_name = django_filters.CharFilter(field_name='province__name', lookup_expr='icontains')
    city_name = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    class Meta:
        model = UserAddress
        fields = ['user_mobile_number', 'province_name', 'city_name']
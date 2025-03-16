import django_filters
from .models import Role, User

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

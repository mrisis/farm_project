import django_filters
from .models import Role

class RoleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = Role
        fields = ['category',]
import django_filters
from apps.locations.models import City


class CityFilter(django_filters.FilterSet):
    province  = django_filters.CharFilter(field_name='province',lookup_expr='exact')
    province_name = django_filters.CharFilter(field_name='province__name',lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['province', 'province_name']

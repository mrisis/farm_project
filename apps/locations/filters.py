import django_filters
from apps.locations.models import City


class CityFilter(django_filters.FilterSet):
    province  = django_filters.CharFilter(field_name='province',lookup_expr='exact')

    class Meta:
        model = City
        fields = ['province']

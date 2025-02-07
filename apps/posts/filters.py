import django_filters
from apps.posts.models import Post


class PostFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = Post
        fields = [
            'min_price',
            'max_price',
            'category',
        ]

import django_filters
from apps.posts import models as post_models


class PostFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = post_models.Post
        fields = [
            'min_price',
            'max_price',
            'category',
        ]





class PostCategoryFilterSet(django_filters.FilterSet):
    just_children = django_filters.BooleanFilter(method="filter_just_children")

    class Meta:
        model = post_models.PostCategory
        fields = [
        ]

    
    def filter_just_children(self, qs, name, value):
        print(value)
        qs.filter(parent__isnull=not(value))
        return qs
            
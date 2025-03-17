import django_filters
from apps.posts import models as post_models


class PostFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    province = django_filters.CharFilter(field_name='address__province', lookup_expr='exact')
    author_mobile_number = django_filters.CharFilter(field_name='author__mobile_number', lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = post_models.Post
        fields = [
            'min_price',
            'max_price',
            'category',
            'province',
            'author_mobile_number',
            'category_name',
        ]





class PostCategoryFilterSet(django_filters.FilterSet):
    parent = django_filters.BooleanFilter(method="filter_parent")
    parent_name = django_filters.CharFilter(field_name='parent__name', lookup_expr='icontains')

    class Meta:
        model = post_models.PostCategory
        fields = ['parent', 'parent_name']

    def filter_parent(self, qs, name, value):
        if value:
            return qs.filter(parent__isnull=True)
        return qs.filter(parent__isnull=False)
    



class PostImageFilterSet(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    author_post_mobile_number = django_filters.CharFilter(field_name='post__author__mobile_number', lookup_expr='icontains')

    class Meta:
        model = post_models.PostImage
        fields = ['post_title', 'author_post_mobile_number']




class PostAddressFilterSet(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    author_post_mobile_number = django_filters.CharFilter(field_name='post__author__mobile_number', lookup_expr='icontains')

    class Meta:
        model = post_models.PostAddress
        fields = ['post_title', 'author_post_mobile_number']
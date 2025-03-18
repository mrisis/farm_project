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




class CommentFilterSet(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    author_mobile_number = django_filters.CharFilter(field_name='author__mobile_number', lookup_expr='icontains')
    author_first_name = django_filters.CharFilter(field_name='author__first_name', lookup_expr='icontains')
    author_last_name = django_filters.CharFilter(field_name='author__last_name', lookup_expr='icontains')
    post_category_name = django_filters.CharFilter(field_name='post__category__name', lookup_expr='icontains')

    class Meta:
        model = post_models.Comment
        fields = ['post_title', 'author_mobile_number', 'author_first_name', 'author_last_name', 'post_category_name']




class RatingFilterSet(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    author_mobile_number = django_filters.CharFilter(field_name='author__mobile_number', lookup_expr='icontains')
    post_category_name = django_filters.CharFilter(field_name='post__category__name', lookup_expr='icontains')

    class Meta:
        model = post_models.Rating
        fields = ['post_title', 'author_mobile_number', 'post_category_name']





class FavoritePostFilterSet(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    user_mobile_number = django_filters.CharFilter(field_name='user__mobile_number', lookup_expr='icontains')

    class Meta:
        model = post_models.FavoritePost
        fields = ['post_title', 'user_mobile_number']

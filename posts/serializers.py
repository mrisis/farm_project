from rest_framework import serializers
from .models import PostCategory

class ParentPostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name', 'slug', 'description']

class PostCategorySerializer(serializers.ModelSerializer):
    parent = ParentPostCategorySerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all(), source='parent',
                                                   write_only=True, allow_null=True, required=False)

    class Meta:
        model = PostCategory
        fields = ['id', 'name', 'slug', 'description', 'parent', 'parent_id']
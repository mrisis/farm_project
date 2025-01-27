from rest_framework import serializers
from .models import PostCategory, Post
from accounts.serializers import UserSerializer
from accounts.models import User

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

    def validate_parent_id(self, value):
        if value == self.instance:
            raise serializers.ValidationError("A category cannot be its own parent.")
        return value


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True)

    category = PostCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all(), source='category',
                                                    write_only=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_id', 'category', 'category_id', 'created_at']




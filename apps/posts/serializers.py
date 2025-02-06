from rest_framework import serializers
from urllib3 import request

from .models import PostCategory, Post, PostImage, Comment, Rating, FavoritePost
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from apps.files.models import Asset
from apps.files.serializers import AssetSerializer
from datetime import timedelta
from django.utils import timezone

class ParentPostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name', 'icon', 'slug', 'description']

class PostCategorySerializer(serializers.ModelSerializer):
    parent = ParentPostCategorySerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all(), source='parent',
                                                   write_only=True, allow_null=True, required=False)

    class Meta:
        model = PostCategory
        fields = ['id', 'name', 'icon', 'slug', 'description', 'parent', 'parent_id']

    def validate_parent_id(self, value):
        if value == self.instance:
            raise serializers.ValidationError("A category cannot be its own parent.")
        return value
class PostImageInoutSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = PostImage
        fields = ['id', 'post', 'post_id', 'asset', 'image', 'caption']

    def validate(self, attrs):
        request = self.context.get('request')
        now = timezone.now()
        one_hour_ago = now - timedelta(minutes=60)

        recent_images = PostImage.objects.filter(
            post__isnull=True,
            asset__owner=request.user,
            created_at__lte=one_hour_ago

        )
        if recent_images.count() >= 100:
            raise serializers.ValidationError("You can only upload 100 images per hour.")

class PostImageOutputSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = PostImage
        fields = ['id', 'post', 'post_id', 'asset', 'caption']



class PostInputSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = PostCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all(), source='category',
                                                    write_only=True, allow_null=True, required=False)
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_id', 'category','images_id', 'category_id', 'created_at']

class PostOutputSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = PostCategorySerializer(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_id', 'category','images', 'category_id', 'created_at']

    def __init__(self, *args,method='list', **kwargs):
        self.method = method
        super().__init__(*args, **kwargs)


    def get_images(self, obj):
        if self.method == 'list':
            images = PostImage.objects.filter(post=obj).first()
            return PostImageOutputSerializer(images).data

        elif self.method == 'detail':
            images = PostImage.objects.filter(post=obj)
            return PostImageOutputSerializer(images, many=True).data





class ParentCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text']


class CommentSerializer(serializers.ModelSerializer):
    post = PostOutputSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True)
    parent = ParentCommentSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent', write_only=True, allow_null=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'text', 'parent', 'parent_id', 'created_at']

    def validate(self, data):
        if data.get('parent') and data['parent'].post != data['post']:
            raise serializers.ValidationError("Parent comment must belong to the same post.")
        return data



class RatingSerializer(serializers.ModelSerializer):
    post = PostOutputSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'score', 'created_at']

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Score must be between 0 and 5.")
        return value

    def validate(self, data):
        post = data.get('post')
        author = data.get('author')
        if Rating.objects.filter(post=post, author=author).exists():
            raise serializers.ValidationError("You have already rated this post.")
        return data


class FavoritePostSerializer(serializers.ModelSerializer):
    post = PostOutputSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = FavoritePost
        fields = ['id', 'post', 'post_id', 'user', 'user_id', 'created_at']

    def validate(self, data):
        post = data.get('post')
        user = data.get('user')
        if FavoritePost.objects.filter(post=post, user=user).exists():
            raise serializers.ValidationError("You have already favorited this post.")
        return data

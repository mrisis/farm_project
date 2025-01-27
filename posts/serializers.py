from rest_framework import serializers
from .models import PostCategory, Post, PostImage
from accounts.serializers import UserSerializer
from accounts.models import User
from files.models import Asset
from files.serializers import AssetSerializer

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


class PostImageSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_data = serializers.JSONField(write_only=True, required=False)
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post', write_only=True)

    class Meta:
        model = PostImage
        fields = ['id', 'post', 'post_id', 'asset', 'asset_data', 'caption']

    def validate(self, attrs):
        asset_data = attrs.get('asset_data')
        if asset_data:
            if not any([asset_data.get('owner'), asset_data.get('file'), asset_data.get('image')]):
                raise serializers.ValidationError({
                    'asset_data': 'At least one of "owner", "file", or "image" must be provided for asset.'
                })
        else:
            raise serializers.ValidationError({
                'asset_data': 'This field is required to create an asset.'
            })
        return attrs

    def create(self, validated_data):
        asset_data = validated_data.pop('asset_data')

        owner_id = asset_data.get('owner')
        if owner_id:
            try:
                asset_data['owner'] = User.objects.get(id=owner_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({'asset_data': 'Invalid owner ID.'})

        asset = Asset.objects.create(**asset_data)

        post_image = PostImage.objects.create(asset=asset, **validated_data)
        return post_image








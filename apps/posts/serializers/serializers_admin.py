from rest_framework import serializers
from apps.posts.models import Post, PostImage, PostCategory, PostAddress
from apps.posts.mixins import ImageUrlMixin
from django.utils import timezone
from datetime import timedelta


class PostListAdminSerializer(serializers.ModelSerializer):
    author_mobile_number = serializers.StringRelatedField(source="author.mobile_number")
    category = serializers.StringRelatedField(source="category.name")
    class Meta:
        model = Post
        fields = ["id", "title", "category", "author_mobile_number"]


class PostDetailAdminSerializer(serializers.ModelSerializer):
    author_mobile_number = serializers.StringRelatedField(source="author.mobile_number")
    category_name = serializers.StringRelatedField(source="category.name")
    images = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable", "author_mobile_number", "category_name", "images"]


    def get_images(self, obj):
        request = self.context.get('request')
        images = PostImage.objects.filter(post=obj)
        return [
            {
                'url': request.build_absolute_uri(image.asset.image.url),
                "id": image.id
            } for image in images
        ]
    


class PostCreateAdminSerializer(serializers.ModelSerializer):
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable", "author", "category", "images_id"]

    def validate(self, attrs):
        is_visible_mobile = attrs.get('is_visible_mobile', False)
        is_chat_avaliable = attrs.get('is_chat_avaliable', False)
        if not (is_visible_mobile or is_chat_avaliable):
            raise serializers.ValidationError("is_visible_mobile and is_chat_avaliable cannot be False at the same time")
        return attrs
    


class PostUpdateAdminSerializer(serializers.ModelSerializer):
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable", "author", "category", "images_id"]

        
    

class PostCategoryListAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name", "icon", "description", "parent"]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = self.get_image_url(instance, 'icon')
        data['parent'] = instance.parent.name if instance.parent else 'بدون دسته بندی پدر'
        data['description'] = instance.description[:50] + '...' if len(instance.description) > 50 else instance.description
        return data



class PostCategoryDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name", "icon", "description", "parent", "slug"]



class PostCategoryCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name", "icon", "description", "parent", "slug"]


class PostCategoryUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name", "icon", "description", "parent", "slug"]




class PostImageListAdminSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(source="post.title")
    author_post_mobile_number = serializers.StringRelatedField(source="post.author.mobile_number")
    class Meta:
        model = PostImage
        fields = ["id", "post", "asset", "caption", "author_post_mobile_number"]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['caption'] = instance.caption[:50] + '...' if instance.caption else 'بدون عنوان'
        return data



class PostImageDetailAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    author_post_mobile_number = serializers.StringRelatedField(source="post.author.mobile_number")
    class Meta:
        model = PostImage
        fields = ["id", "post", "asset", "caption", "author_post_mobile_number"]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['asset'] = self.get_image_url(instance, 'asset')
        return data


class PostImageCreateAdminSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)
    mobile_number = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = PostImage
        fields = ["id", "post", "image", "caption", "mobile_number"]
        
        extra_kwargs = {
            'post': {'required': True},
            }

    def validate(self, attrs):
        request = self.context.get('request')

        recent_images = PostImage.objects.filter(
            post__isnull=True,
            created_at__lte=timezone.now() - timedelta(minutes=60)
        )
        if recent_images.count() >= 100:
            raise serializers.ValidationError("You can only upload 100 images per hour.")
        return attrs




class PostAddressListAdminSerializer(serializers.ModelSerializer):
    author_post_mobile_number = serializers.StringRelatedField(source="post.author.mobile_number")
    province = serializers.StringRelatedField(source="province.name")
    post = serializers.StringRelatedField(source="post.title")
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "author_post_mobile_number"]


class PostAddressDetailAdminSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(source="post.title")
    province = serializers.StringRelatedField(source="province.name")
    city = serializers.StringRelatedField(source="city.name")
    author_post_mobile_number = serializers.StringRelatedField(source="post.author.mobile_number")
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code", "author_post_mobile_number"]



class PostAddressCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code"]


class PostAddressUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code"]








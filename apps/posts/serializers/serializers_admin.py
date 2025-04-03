from rest_framework import serializers
from apps.posts.models import Post, PostImage, PostCategory, PostAddress, Comment, Rating, FavoritePost
from apps.locations.models import Province, City
from apps.posts.mixins import ImageUrlMixin
from django.utils import timezone
from datetime import timedelta


class PostListAdminSerializer(serializers.ModelSerializer):
    author_mobile_number = serializers.StringRelatedField(source="author.mobile_number")
    category = serializers.StringRelatedField(source="category.name")

    class Meta:
        model = Post
        fields = ["id", "title", "category", "author_mobile_number", "status"]


class ProvinceNestedAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class CityNestedAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class PostAddressNestedAdminSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostAddress
        fields = ['id', 'full_address', 'postal_code', 'province', 'city']

    def get_province(self, obj):
        return ProvinceNestedAdminSerializer(obj.province).data

    def get_city(self, obj):
        return CityNestedAdminSerializer(obj.city).data


class PostDetailAdminSerializer(serializers.ModelSerializer):
    author_mobile_number = serializers.StringRelatedField(source="author.mobile_number")
    category = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField()
    total_seconds = serializers.SerializerMethodField(read_only=True)
    address = PostAddressNestedAdminSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable",
                  "author_mobile_number", "category", "images", 'total_seconds', 'address']

    def get_total_seconds(self, obj):
        return obj.get_total_seconds()

    def get_images(self, obj):
        request = self.context.get('request')
        images = PostImage.objects.filter(post=obj)
        return [
            {
                'url': request.build_absolute_uri(image.asset.image.url),
                "id": image.id
            } for image in images
        ]

    def get_category(self, obj):
        return {

            "id": obj.category.id,
            "name": obj.category.name,
        }


class PostCreateAdminSerializer(serializers.ModelSerializer):
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable", "author",
                  "category", "images_id"]

    def validate(self, attrs):
        is_visible_mobile = attrs.get('is_visible_mobile', False)
        is_chat_avaliable = attrs.get('is_chat_avaliable', False)
        if not (is_visible_mobile or is_chat_avaliable):
            raise serializers.ValidationError(
                "is_visible_mobile and is_chat_avaliable cannot be False at the same time")
        return attrs


class PostUpdateAdminSerializer(serializers.ModelSerializer):
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "unit_price", "price", "is_visible_mobile", "is_chat_avaliable", "author",
                  "category", "images_id"]


class PostCategoryListAdminSerializer(ImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name", "icon", "description", "parent"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = self.get_image_url(instance, 'icon')
        data['parent'] = instance.parent.name if instance.parent else None
        data['description'] = instance.description[:50] + '...' if instance.description and len(
            instance.description) > 50 else instance.description
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

    def validate_parent(self, value):
        if self.instance and self.instance.parent is None and value is not None:
            raise serializers.ValidationError("Cannot assign a parent to a top-level category.")


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
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code",
                  "author_post_mobile_number"]


class PostAddressCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code"]


class PostAddressUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = ["id", "post", "province", "city", "lat", "lng", "full_address", "postal_code"]


class PostCommentListAdminSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(source="post.title")
    author = serializers.StringRelatedField(source="author.mobile_number")

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "parent"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['text'] = instance.text[:50] + '...' if instance.text else 'بدون نظر'
        return data


class PostCommentDetailAdminSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "parent"]

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "mobile_number": obj.author.mobile_number,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
            "email": obj.author.email,

        }

    def get_post(self, obj):
        return {
            "id": obj.post.id,
            "title": obj.post.title,
            "category": obj.post.category.name,
        }


class PostCommentCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "parent"]


class PostCommentUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "parent"]


class PostRatingListAdminSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(source="post.title")
    author = serializers.StringRelatedField(source="author.mobile_number")

    class Meta:
        model = Rating
        fields = ["id", "post", "author", "score"]


class PostRatingDetailAdminSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ["id", "post", "author", "score"]

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "mobile_number": obj.author.mobile_number,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
        }

    def get_post(self, obj):
        return {
            "id": obj.post.id,
            "title": obj.post.title,
            "category": obj.post.category.name,
        }


class PostRatingCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "post", "author", "score"]


class PostRatingUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "post", "author", "score"]


class FavoritePostListAdminSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(source="post.title")
    user = serializers.StringRelatedField(source="user.mobile_number")

    class Meta:
        model = FavoritePost
        fields = ["id", "post", "user"]


class FavoritePostDetailAdminSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = FavoritePost
        fields = ["id", "post", "user"]

    def get_post(self, obj):
        return {
            "id": obj.post.id,
            "title": obj.post.title,
            "category": obj.post.category.name,
        }

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "mobile_number": obj.user.mobile_number,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }


class FavoritePostCreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePost
        fields = ["id", "post", "user"]


class FavoritePostUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePost
        fields = ["id", "post", "user"]


class PostStatusUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "status", "rejection_reason", "rejection_details"]

    def validate(self, data):
        if data.get('status') == Post.PostStatus.REJECTED:
            if not data.get('rejection_reason'):
                raise serializers.ValidationError(
                    "rejection_reason is required when status is REJECTED"
                )
        return data

    def update(self, instance, validated_data):
        if validated_data.get('status') == Post.PostStatus.APPROVED:
            validated_data['rejection_reason'] = None
            validated_data['rejection_details'] = None
        return super().update(instance, validated_data)


class PostCountAdminSerializer(serializers.Serializer):
    total_posts = serializers.IntegerField()
    new_posts = serializers.IntegerField()
    approved_posts = serializers.IntegerField()
    rejected_posts = serializers.IntegerField()

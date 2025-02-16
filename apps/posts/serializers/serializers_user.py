from rest_framework import serializers
from apps.posts.models import PostCategory, PostImage, Post, PostAddress, Rating, Comment, FavoritePost
from apps.files.serializers import AssetSerializer
from datetime import timedelta
from django.utils import timezone
from apps.locations.models import Province, City
import jdatetime
from django.utils.timezone import now


class SubcategoriesNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name', 'icon']


class PostCategoryListUserSerializer(serializers.ModelSerializer):
    subcategories = SubcategoriesNestedSerializer(many=True, read_only=True)

    class Meta:
        model = PostCategory
        fields = [
            'id', 'name', 'icon', 'slug', 'description', 'subcategories',

        ]


class PostImageListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = None
        if instance.asset is not None:
            data['image'] = instance.asset.image.url

        return data


class PostCategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'name']


class ProvinceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class CityNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class PostAddressNestedSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostAddress
        fields = ['id', 'full_address', 'postal_code', 'province', 'city']

    def get_province(self, obj):
        return ProvinceNestedSerializer(obj.province).data

    def get_city(self, obj):
        return CityNestedSerializer(obj.city).data


class PostListUserSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    category = PostCategoryNestedSerializer(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    address = PostAddressNestedSerializer(read_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    total_seconds = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'is_favorite', 'category', 'price', 'address', 'images', 'ratings',
                  'created_at', 'total_seconds']

    def __init__(self, *args, method='list', **kwargs):
        fields = kwargs.pop('only_fields', None)

        self.method = method
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_images(self, obj):
        if self.method == 'list':
            images = PostImage.objects.filter(post=obj).first()
            return PostImageListUserSerializer(images).data

        elif self.method == 'detail':
            images = PostImage.objects.filter(post=obj)
            return PostImageListUserSerializer(images, many=True).data

    def get_author(self, obj):
        if obj.is_visible_mobile:

            return {
                'mobile_number': obj.author.mobile_number
            }
        else:
            return {
                'first_name': obj.author.first_name,
                'last_name': obj.author.last_name
            }

    def get_ratings(self, obj):
        ratings_score = self.context.get('ratings_score')
        ratings_count = self.context.get('ratings_count')
        return {
            'avg_score': ratings_score,
            'vote_counts': ratings_count.get('value', None)
        }

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def get_total_seconds(self, obj):
        return int((now() - obj.created_at).total_seconds())


class PostCreateUpdateUserSerializer(serializers.ModelSerializer):
    images_id = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=False)
    full_address = serializers.CharField(write_only=True, required=False)
    province = serializers.IntegerField(write_only=True, required=False)
    city = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'category', 'unit_price', 'price', 'images_id', 'full_address', 'province',
                  'city', 'is_visible_mobile', 'is_chat_avaliable', 'created_at']

    def validate(self, attrs):
        if attrs.get('is_visible_mobile', False) is False and attrs.get('is_chat_avaliable', False) is False:
            raise serializers.ValidationError("ChatValidation")
        return attrs


class PostImageCreateUserSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = PostImage
        fields = ['id', 'post', 'asset', 'image', 'caption']

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
        return attrs


class PostCommentRateUserSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created_at_shamsi = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'parent', 'rating', 'created_at', 'created_at_shamsi']

    def get_rating(self, obj):
        post_id = obj.post.id
        user = obj.author

        rating = Rating.objects.filter(post_id=post_id, author=user).first()
        return rating.score if rating else None

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
        }

    def get_created_at_shamsi(self, obj):
        if obj.created_at:
            shamsi_date = jdatetime.datetime.fromgregorian(datetime=obj.created_at)
            return shamsi_date.strftime("%Y-%m-%d")


class PostCommentRateCreateUserSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'parent', 'score', 'created_at']


class PostAddToFavoriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePost
        fields = ['id', 'post']

class RatingCheckSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
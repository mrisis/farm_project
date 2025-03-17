from rest_framework import serializers
from apps.posts.models import Post, PostImage


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

        
    


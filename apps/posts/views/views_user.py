from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.posts.models import PostCategory, Post, PostImage, PostAddress, Rating, Comment, FavoritePost
from apps.files.models import Asset
from apps.posts.serializers.serializers_user import PostCategoryListUserSerializer, PostListUserSerializer, PostCreateUpdateUserSerializer, \
    PostImageCreateUserSerializer, PostCommentRateUserSerializer, PostCommentRateCreateUserSerializer, PostAddToFavoriteUserSerializer
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from django.db.models import Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from apps.posts import filters as post_filters
from rest_framework.filters import SearchFilter, OrderingFilter


class PostCategoryListApiView(GenericAPIView):
    serializer_class = PostCategoryListUserSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = post_filters.PostCategoryFilterSet
    
    def get(self, request):
        categorie_qs = self.filter_queryset(PostCategory.objects.all())
        serializer = self.get_serializer(categorie_qs, many=True)
        return Response(serializer.data)


class PostListUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = post_filters.PostFilter
    search_fields = ['title', 'category__name']
    ordering_fields = ['price',]
    ordering = ['-created_at']

    def get(self, request):
        posts_qs = self.filter_queryset(Post.objects.all())
        page = self.paginate_queryset(posts_qs)
        serializer = self.get_serializer(page, many=True, method='list', only_fields={
            'id',
            'title',
            'price',
            'images',
            'address',
            'created_at',
        })
        return self.get_paginated_response(serializer.data)

class PostDetailUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        ratings_post = post.ratings.all().aggregate(Avg('score'))
        ratings_count = post.ratings.all().aggregate(value=Count('id'))
        serializer = self.get_serializer(post, method='detail',
                                         context={'ratings_post': ratings_post, 'ratings_count': ratings_count})
        return Response(serializer.data)


class PostCreateUserApiView(GenericAPIView):
    serializer_class = PostCreateUpdateUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images_id = serializer.validated_data.get('images_id', None)
        province = serializer.validated_data.get('province', None)
        city = serializer.validated_data.get('city', None)
        full_address = serializer.validated_data.get('full_address', None)
        post_image = PostImage.objects.filter(id__in=images_id)

        post = Post(
            title=serializer.validated_data.get('title', None),
            author=request.user,
            body=serializer.validated_data.get('body', None),
            category=serializer.validated_data.get('category', None),
            price=serializer.validated_data.get('price', None),
            is_visible_mobile=serializer.validated_data.get('is_visible_mobile', False),
            is_chat_avaliable=serializer.validated_data.get('is_chat_avaliable', False),
        )
        post.save()
        post_address = PostAddress(
            post=post,
            province_id=province,
            city_id=city,
            full_address=full_address,
        )
        post_address.save()
        post.images.set(post_image)

        return Response({"message": "Post Created Successfully"}, status=status.HTTP_201_CREATED)


class PostUpdateUserApiView(GenericAPIView):
    serializer_class = PostCreateUpdateUserSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        images_id = serializer.validated_data.get('images_id', None)
        post_images = post.images.all()
        if len(images_id) >= 3:
            return Response({"detail": "Maximum 3 images allowed."}, status=status.HTTP_400_BAD_REQUEST)
        for image in post_images:
            if image.id not in images_id:
                if image.asset is not None:
                    image.asset.delete()
                image.delete()

        post_images_obj = PostImage.objects.filter(id__in=images_id)
        post.images.set(post_images_obj)

        serializer.save()
        return Response(serializer.data)


class PostDeleteUserApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post_images = post.images.all()
        for image in post_images:
            if image.asset is not None:
                image.asset.delete()
            image.delete()

        post.delete()
        return Response({"detail": "PostDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)


class PostImageCreateUserApiView(GenericAPIView):
    serializer_class = PostImageCreateUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('image', None)

        asset = Asset(
            title='post image',
            owner=request.user,
            image=image,
        )
        asset.save()
        post_image = PostImage.objects.create(
            asset=asset,
        )
        return Response({'image_id': post_image.id}, status=status.HTTP_201_CREATED)


class PostCommentRateListUserApiView(GenericAPIView):
    serializer_class = PostCommentRateUserSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all()

        serializer = self.get_serializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCommentRateCreateUserApiView(GenericAPIView):
    serializer_class = PostCommentRateCreateUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data.get('post')
        parent = serializer.validated_data.get('parent')

        score = serializer.validated_data.get('score', None)
        if score is not None:
            Rating.objects.create(post=post, author=request.user, score=score)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=serializer.validated_data.get('text'),
            parent=parent
        )

        return Response({"detail": "Comment and Rating Created Successfully"}, status=status.HTTP_201_CREATED)


class PostAddToFavoriteUserApiView(GenericAPIView):
    serializer_class = PostAddToFavoriteUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data.get('post')
        favorite_post = FavoritePost(
            post=post,
            user=request.user,
        )
        favorite_post.save()

        return Response({"detail": "Post Added to Favorites Successfully"}, status=status.HTTP_201_CREATED)
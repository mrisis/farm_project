from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.posts.models import PostCategory, Post, PostImage, PostAddress, Rating, Comment, FavoritePost
from apps.files.models import Asset
from apps.posts.serializers.serializers_user import PostCategoryListUserSerializer, PostListUserSerializer, \
    PostCreateUpdateUserSerializer, \
    PostImageCreateUserSerializer, PostCommentRateUserSerializer, PostCommentRateCreateUserSerializer, \
    PostAddToFavoriteUserSerializer, RatingCheckSerializer
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
        categorie_qs = self.filter_queryset(PostCategory.objects.all().order_by('id'))
        serializer = self.get_serializer(categorie_qs, many=True)
        return Response(serializer.data)


class PostListUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = post_filters.PostFilter
    search_fields = ['title', 'category__name']
    ordering_fields = ['price', ]
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
        ratings_score = post.ratings.all().aggregate(Avg('score'))
        ratings_count = post.ratings.all().aggregate(value=Count('id'))
        context = self.get_serializer_context()
        context.update({
            'ratings_score': ratings_score,
            'ratings_count': ratings_count
        })
        serializer = self.get_serializer(post, method='detail', context=context)
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
        comments = post.comments.all().order_by('-created_at')

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
            existing_rating = Rating.objects.filter(post=post, author=request.user).first()
            if existing_rating:
                return Response({"detail": "YouHaveAlreadyRatedThisPost"}, status=status.HTTP_400_BAD_REQUEST)
            Rating.objects.create(post=post, author=request.user, score=score)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=serializer.validated_data.get('text'),
            parent=parent
        )
        comment.save()

        return Response({"detail": "Comment and Rating Created Successfully"}, status=status.HTTP_201_CREATED)


class PostAddOrRemoveToFavoriteUserApiView(GenericAPIView):
    serializer_class = PostAddToFavoriteUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data.get('post')
        favorit_qs = FavoritePost.objects.filter(post=post, user=request.user)
        if favorit_qs.exists():
            favorit_qs.delete()
            return Response({"detail": False}, status=status.HTTP_200_OK)
        else:
            favorite_post = FavoritePost(
                post=post,
                user=request.user,
            )
            favorite_post.save()

            return Response({"detail": True}, status=status.HTTP_201_CREATED)


class MyFavoritePostListUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = post_filters.PostFilter
    search_fields = ['title', 'category__name']
    ordering_fields = ['price', ]
    ordering = ['-created_at']

    def get(self, request):
        posts_qs = self.filter_queryset(Post.objects.filter(favorites__user=request.user))
        page = self.paginate_queryset(posts_qs)
        serializer = self.get_serializer(page, many=True, method='list', only_fields={
            'id',
            'title',
            'images',
            'address',
            'price',
            'created_at',
        })
        return self.get_paginated_response(serializer.data)



class MyFavoritePostDetailUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk, favorites__user=request.user)
        ratings_score = post.ratings.all().aggregate(Avg('score'))
        ratings_count = post.ratings.all().aggregate(value=Count('id'))
        context = self.get_serializer_context()
        context.update({
            'ratings_score': ratings_score,
            'ratings_count': ratings_count
        })
        serializer = self.get_serializer(post, method='detail', context=context)
        return Response(serializer.data)


class MyPostListUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = post_filters.PostFilter
    search_fields = ['title', 'category__name']
    ordering_fields = ['price', ]
    ordering = ['-created_at']

    def get(self, request):
        posts_qs = self.filter_queryset(Post.objects.filter(author=request.user))
        page = self.paginate_queryset(posts_qs)
        serializer = self.get_serializer(page, many=True, method='list', only_fields={
            'id',
            'title',
            'images',
            'address',
            'price',
            'created_at',
        })
        return self.get_paginated_response(serializer.data)


class MyPostDetailUserApiView(GenericAPIView):
    serializer_class = PostListUserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        ratings_score = post.ratings.all().aggregate(Avg('score'))
        ratings_count = post.ratings.all().aggregate(value=Count('id'))
        context = self.get_serializer_context()
        context.update({
            'ratings_score': ratings_score,
            'ratings_count': ratings_count
        })
        serializer = self.get_serializer(post, method='detail', context=context)
        return Response(serializer.data)



class RatingCheckUserApiView(GenericAPIView):
    serializer_class = RatingCheckSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.validated_data.get('post')
        rating = Rating.objects.filter(post=post, author=request.user).first()
        if rating:
            return Response({"has_rated": True}, status=status.HTTP_200_OK)
        else:
            return Response({"has_rated": False}, status=status.HTTP_200_OK)


class MyPostDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        post_images = post.images.all()
        for image in post_images:
            if image.asset is not None:
                image.asset.delete()
            image.delete()

        post.delete()
        return Response({"detail": "PostDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)


class PostImageRemoveApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk, *args, **kwargs):
        try:
            post_image = PostImage.objects.select_related('post').get(pk=pk)
        except PostImage.DoesNotExist:
            return Response({"detail": "PostImageNotFound"}, status=status.HTTP_404_NOT_FOUND)

        if post_image.post.author != request.user:
            return Response({"detail": "YouAreNotTheAuthorOfThisPost"}, status=status.HTTP_403_FORBIDDEN)
        if post_image.asset is not None:
            post_image.asset.delete()
            post_image.delete()
            return Response({"detail": "PostImageRemovedSuccessfully"}, status=status.HTTP_200_OK)

        return Response({"detail": "PostImageNotFound"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.generics import GenericAPIView
from apps.posts.serializers.serializers_admin import PostListAdminSerializer, PostDetailAdminSerializer, PostCreateAdminSerializer, PostUpdateAdminSerializer
from rest_framework.permissions import IsAdminUser
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.posts.models import Post, PostImage
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from apps.posts.filters import PostFilter


class PostListAdminView(GenericAPIView):
    serializer_class = PostListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'author__mobile_number', 'category__name']

    def get(self, request):
        posts = Post.objects.all()
        posts_qs = self.filter_queryset(posts)
        page = self.paginate_queryset(posts_qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    



class PostDetailAdminView(GenericAPIView):
    serializer_class = PostDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostCreateAdminView(GenericAPIView):
    serializer_class = PostCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images_id = serializer.validated_data.get('images_id', None)
        post_images = PostImage.objects.filter(id__in = images_id)

        post = Post(
            title=serializer.validated_data.get('title'),
            body=serializer.validated_data.get('body'),
            unit_price=serializer.validated_data.get('unit_price'),
            price=serializer.validated_data.get('price'),
            is_visible_mobile=serializer.validated_data.get('is_visible_mobile'),
            is_chat_avaliable=serializer.validated_data.get('is_chat_avaliable'),
            author=request.user,
            category=serializer.validated_data.get('category'),
        )
        post.save()
        post.images.set(post_images)
        return Response({"message": "Post Created Successfully"}, status=status.HTTP_201_CREATED)




class PostUpdateAdminView(GenericAPIView):
    serializer_class = PostUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        images_id = serializer.validated_data.get('images_id', None)
        post_images = post.images.all()
        if len(images_id) >= 3:
            return Response({"detail": "Maximum 3 images allowed."}, status=status.HTTP_400_BAD_REQUEST)
        for image in post_images:
            if image.id not in images_id:
                image.delete()
        post_images_obj = PostImage.objects.filter(id__in=images_id)
        post.images.set(post_images_obj)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDeleteAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_images = post.images.all()
        for image in post_images:
            if image.asset is not None:
                image.asset.delete()
            image.delete()
        post.delete()
        return Response({"message": "Post Deleted Successfully"}, status=status.HTTP_200_OK)
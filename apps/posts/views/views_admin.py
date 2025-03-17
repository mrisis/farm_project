from rest_framework.generics import GenericAPIView
from apps.posts.serializers.serializers_admin import PostListAdminSerializer, PostDetailAdminSerializer, PostCreateAdminSerializer, PostUpdateAdminSerializer, PostCategoryListAdminSerializer, PostCategoryDetailAdminSerializer, PostCategoryCreateAdminSerializer, PostCategoryUpdateAdminSerializer, PostImageListAdminSerializer, PostImageDetailAdminSerializer, PostImageCreateAdminSerializer
from rest_framework.permissions import IsAdminUser
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.posts.models import Post, PostImage, PostCategory
from apps.files.models import Asset
from apps.accounts.models import User
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from apps.posts.filters import PostFilter, PostCategoryFilterSet, PostImageFilterSet


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
    


class PostCategoryListAdminView(GenericAPIView):
    serializer_class = PostCategoryListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostCategoryFilterSet
    search_fields = ['name', 'parent__name']

    def get(self, request):
        categories = PostCategory.objects.all()
        categories_qs = self.filter_queryset(categories)
        page = self.paginate_queryset(categories_qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    



class PostCategoryDetailAdminView(GenericAPIView):
    serializer_class = PostCategoryDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        category = get_object_or_404(PostCategory, pk=pk)
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class PostCategoryCreateAdminView(GenericAPIView):
    serializer_class = PostCategoryCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_category = PostCategory(
            name=serializer.validated_data.get('name'),
            icon=serializer.validated_data.get('icon'),
            description=serializer.validated_data.get('description'),
            parent=serializer.validated_data.get('parent'),
            slug=serializer.validated_data.get('slug'),
        )
        post_category.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class PostCategoryUpdateAdminView(GenericAPIView):
    serializer_class = PostCategoryUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(PostCategory, pk=pk)
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostCategoryDeleteAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        category = get_object_or_404(PostCategory, pk=pk)
        category.delete()
        return Response({"message": "Post Category Deleted Successfully"}, status=status.HTTP_200_OK)
    



class PostImageListAdminView(GenericAPIView):
    serializer_class = PostImageListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostImageFilterSet
    search_fields = ['post__title', 'post__author__mobile_number']

    def get(self, request):
        images = PostImage.objects.all()
        images_qs = self.filter_queryset(images)
        page = self.paginate_queryset(images_qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)



class PostImageDetailAdminView(GenericAPIView):
    serializer_class = PostImageDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        image = get_object_or_404(PostImage, pk=pk)
        serializer = self.get_serializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class PostImageCreateAdminView(GenericAPIView):
    serializer_class = PostImageCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data.get('image', None)
        mobile_number = serializer.validated_data.get('mobile_number', None)
        author = get_object_or_404(User, mobile_number=mobile_number)

        post_id = serializer.validated_data.get('post').id
        post = Post.objects.get(pk = post_id)
        if post.author.mobile_number != author.mobile_number:
            return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)

        asset = Asset(
            title='post image',
            owner=author,
            image=image,
        )
        asset.save()

        post_image = PostImage(
            asset=asset,
            caption=serializer.validated_data.get('caption'),
            post=serializer.validated_data.get('post'),
        )
        post_image.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class PostImageDeleteAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        post_image = get_object_or_404(PostImage, pk=pk)
        if post_image.asset is not None:
            post_image.asset.delete()
        post_image.delete()
        return Response({"message": "Post Image Deleted Successfully"}, status=status.HTTP_200_OK)
            
        
        

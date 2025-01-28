from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PostCategory, Post, PostImage, Comment, Rating
from .serializers import PostCategorySerializer, PostSerializer, PostImageSerializer, CommentSerializer, RatingSerializer
from rest_framework.generics import GenericAPIView



class PostCategoryCreateApiView(GenericAPIView):
    serializer_class = PostCategorySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostCategoryListApiView(GenericAPIView):
    serializer_class = PostCategorySerializer
    def get(self, request):
        categories = PostCategory.objects.all()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class PostCategoryDetailApiView(GenericAPIView):
    serializer_class = PostCategorySerializer
    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(PostCategory, pk=pk)
        serializer = self.get_serializer(category)
        return Response(serializer.data)


class PostCategoryUpdateApiView(GenericAPIView):
    serializer_class = PostCategorySerializer
    def put(self, request, pk, *args, **kwargs):
        category = get_object_or_404(PostCategory, pk=pk)
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostCategoryDeleteApiView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(PostCategory, pk=pk)
        category.delete()
        return Response({"detail": "CategoryDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)


class PostCreateApiView(GenericAPIView):
    serializer_class = PostSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListApiView(GenericAPIView):
    serializer_class = PostSerializer
    def get(self, request):
        posts = Post.objects.all()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class PostDetailApiView(GenericAPIView):
    serializer_class = PostSerializer
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class PostUpdateApiView(GenericAPIView):
    serializer_class = PostSerializer
    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PostDeleteApiView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"detail": "PostDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)



class PostImageCreateApiView(GenericAPIView):
    serializer_class = PostImageSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PostImageListApiView(GenericAPIView):
    serializer_class = PostImageSerializer
    def get(self, request, post_id):
        post_images = PostImage.objects.filter(post_id=post_id)
        serializer = self.get_serializer(post_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageUpdateApiView(GenericAPIView):
    serializer_class = PostImageSerializer
    def put(self, request, post_image_id):
        try:
            post_image = PostImage.objects.get(id=post_image_id)
        except PostImage.DoesNotExist:
            return Response({"detail": "PostImageNotFound."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(post_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImageDeleteApiView(APIView):
    def delete(self, request, post_image_id):
        try:
            post_image = PostImage.objects.get(id=post_image_id)
        except PostImage.DoesNotExist:
            return Response({"detail": "PostImageNotFound."}, status=status.HTTP_404_NOT_FOUND)

        post_image.delete()
        return Response({"detail": "PostImageDeletedSuccessfully."}, status=status.HTTP_204_NO_CONTENT)


class CommentCreateApiView(GenericAPIView):
    serializer_class = CommentSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailApiView(GenericAPIView):
    serializer_class = CommentSerializer
    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)


class CommentListApiView(GenericAPIView):
    serializer_class = CommentSerializer
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentUpdateApiView(GenericAPIView):
    serializer_class = CommentSerializer
    def put(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentDeleteApiView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"detail": "CommentDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)


class RatingCreateApiView(GenericAPIView):
    serializer_class = RatingSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RatingDetailApiView(GenericAPIView):
    serializer_class = RatingSerializer
    def get(self, request, pk, *args, **kwargs):
        rating = get_object_or_404(Rating, pk=pk)
        serializer = self.get_serializer(rating)
        return Response(serializer.data)


class RatingListApiView(GenericAPIView):
    serializer_class = RatingSerializer
    def get(self, request, post_id):
        ratings = Rating.objects.filter(post_id=post_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingDeleteApiView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        rating = get_object_or_404(Rating, pk=pk)
        rating.delete()
        return Response({"detail": "RatingDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)











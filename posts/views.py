from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PostCategory
from .serializers import PostCategorySerializer
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

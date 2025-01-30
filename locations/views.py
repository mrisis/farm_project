from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Province
from .serializers import ProvinceSerializer


class ProvinceCreateApiView(GenericAPIView):
    serializer_class = ProvinceSerializer
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProvinceDetailApiView(GenericAPIView):
    serializer_class = ProvinceSerializer
    def get(self,request,pk):
        province = get_object_or_404(Province,pk=pk)
        serializer = self.get_serializer(province)
        return Response(serializer.data)


class ProvinceListApiView(GenericAPIView):
    serializer_class = ProvinceSerializer
    def get(self,request):
        provinces = Province.objects.all()
        serializer = self.get_serializer(provinces,many=True)
        return Response(serializer.data)

class ProvinceUpdateApiView(GenericAPIView):
    serializer_class = ProvinceSerializer
    def put(self,request,pk):
        province = get_object_or_404(Province,pk=pk)
        serializer = self.get_serializer(province,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProvinceDeleteApiView(APIView):
    def delete(self,request,pk):
        province = get_object_or_404(Province,pk=pk)
        province.delete()
        return Response({"detail": "ProvinceDeletedSuccessfully"}, status=status.HTTP_204_NO_CONTENT)


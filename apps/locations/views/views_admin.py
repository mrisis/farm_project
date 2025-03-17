from rest_framework.generics import GenericAPIView
from apps.locations.serializers.serializers_admin import ProvinceListAdminSerializer, ProvinceDetailAdminSerializer, ProvinceCreateAdminSerializer, ProvinceUpdateAdminSerializer
from apps.locations.models import Province
from rest_framework.response import Response
from rest_framework import status   
from rest_framework.permissions import IsAdminUser
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from django.shortcuts import get_object_or_404

class ProvinceListAdminView(GenericAPIView):
    serializer_class = ProvinceListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        provinces = Province.objects.all()
        page = self.paginate_queryset(provinces)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    


class ProvinceDetailAdminView(GenericAPIView):
    serializer_class = ProvinceDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        province = get_object_or_404(Province, pk=pk)
        serializer = self.get_serializer(province)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
class ProvinceCreateAdminView(GenericAPIView):
    serializer_class = ProvinceCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        province = Province(
            name=serializer.validated_data.get("name"),
            code=serializer.validated_data.get("code"),
        )
        province.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

class ProvinceUpdateAdminView(GenericAPIView):
    serializer_class = ProvinceUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        province = get_object_or_404(Province, pk=pk)
        serializer = self.get_serializer(province, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class ProvinceDeleteAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        province = get_object_or_404(Province, pk=pk)
        province.delete()
        return Response({"message": "Province deleted successfully"}, status=status.HTTP_200_OK)
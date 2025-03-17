from rest_framework.generics import GenericAPIView
from apps.locations.serializers.serializers_admin import ProvinceListAdminSerializer, ProvinceDetailAdminSerializer
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
        
        
        

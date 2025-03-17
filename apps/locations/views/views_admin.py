from rest_framework.generics import GenericAPIView
from apps.locations.serializers.serializers_admin import ProvinceListAdminSerializer
from apps.locations.models import Province
from rest_framework.response import Response
from rest_framework import status   
from rest_framework.permissions import IsAdminUser
from core.utils.C_drf.C_paginations import CustomPageNumberPagination


class ProvinceListAdminView(GenericAPIView):
    serializer_class = ProvinceListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        provinces = Province.objects.all()
        page = self.paginate_queryset(provinces)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
        
        
        

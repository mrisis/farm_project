from rest_framework.generics import GenericAPIView
from apps.locations.serializers.serializers_admin import ProvinceListAdminSerializer, ProvinceDetailAdminSerializer, \
    ProvinceCreateAdminSerializer, ProvinceUpdateAdminSerializer, CityListAdminSerializer, CityDetailAdminSerializer, \
    CityCreateAdminSerializer, CityUpdateAdminSerializer
from apps.locations.models import Province, City
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from apps.locations.filters import CityFilter


class ProvinceListAdminView(GenericAPIView):
    serializer_class = ProvinceListAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']
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


class CityListAdminView(GenericAPIView):
    serializer_class = CityListAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CityFilter
    search_fields = ['name', 'province__name']

    def get(self, request):
        cities = City.objects.all()
        cities_qs = self.filter_queryset(cities)
        page = self.paginate_queryset(cities_qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CityDetailAdminView(GenericAPIView):
    serializer_class = CityDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        serializer = self.get_serializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityCreateAdminView(GenericAPIView):
    serializer_class = CityCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = City(
            name=serializer.validated_data.get("name"),
            province=serializer.validated_data.get("province"),
        )
        city.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CityUpdateAdminView(GenericAPIView):
    serializer_class = CityUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        serializer = self.get_serializer(city, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityDeleteAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        city.delete()
        return Response({"message": "City deleted successfully"}, status=status.HTTP_200_OK)

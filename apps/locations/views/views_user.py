from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.locations.models import Province, City
from apps.locations.serializers.serializers_user import ProvinceSerializer, CitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.locations.filters import CityFilter




class ProvinceListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination


    serializer_class = ProvinceSerializer
    def get(self,request):
        provinces =  Province.objects.all()
        serializer = self.get_serializer(provinces,many=True)
        return Response(serializer.data)


class CityListApiView(GenericAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter
    pagination_class = CustomPageNumberPagination
    serializer_class = CitySerializer
    def get(self,request):
        cities = self.filter_queryset(City.objects.all())
        serializer = self.get_serializer(cities,many=True)
        return Response(serializer.data)
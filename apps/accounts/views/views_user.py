from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User, OtpCode, RoleCategory, Role, UserAddress
from apps.accounts.serializers.serializers_user import SendOtpCodeSerializer, VerifyOtpCodeSerializer, \
    UserSignupSerializer, RoleCategorySerializer, RoleSerializer, UserAddressListSerializer, UserRolesListSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts.filters import RoleFilter
from core.utils.C_drf.C_paginations import CustomPageNumberPagination


class SendOtpApiView(GenericAPIView):
    serializer_class = SendOtpCodeSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        try:
            user = get_object_or_404(User, mobile_number=mobile_number)
        except Http404:
            return Response({"message": "user dose not exist"}, status=status.HTTP_400_BAD_REQUEST)
        user.create_and_send_otp()
        return Response({'message': 'OTP_CodeSentSuccessfully'}, status=status.HTTP_200_OK)


class VerifyOtpApiView(GenericAPIView):
    serializer_class = VerifyOtpCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        otp_code = serializer.validated_data['otp_code']
        otp = OtpCode.objects.filter(
            mobile_number=mobile_number,
            otp_code=otp_code,
            is_verified=False
        ).first()
        if not otp or not otp.verify_otp_code(otp_code):
            return Response({'message': 'InvalidOrExpiredOTP_Code'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(mobile_number=mobile_number)
        refresh = RefreshToken.for_user(user)
        data = {
            'message': 'OTP_VerifiedSuccessfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)


class UserSignupApiView(GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        user = User.objects.create(mobile_number=mobile_number, first_name=first_name, last_name=last_name)
        user.create_and_send_otp()
        return Response({'message': 'UserCreatedSuccessfully'}, status=status.HTTP_201_CREATED)


class RoleCategoryListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = RoleCategorySerializer

    def get(self, request):
        role_categories = RoleCategory.objects.all()
        serializer = self.get_serializer(role_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoleFilter

    serializer_class = RoleSerializer

    def get(self, request):
        roles = self.filter_queryset(Role.objects.all())
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAddressListSerializer

    def get(self, request):
        user_addresses = UserAddress.objects.filter(user=request.user)
        serializer = self.get_serializer(user_addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRolesListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserRolesListSerializer

    def get(self, request):
        user_roles = request.user.user_roles.all()
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
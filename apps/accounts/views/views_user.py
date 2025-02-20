from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User, OtpCode, RoleCategory, Role, UserAddress, UserRole
from apps.accounts.serializers.serializers_user import SendOtpCodeSerializer, VerifyOtpCodeSerializer, \
    UserSignupSerializer, RoleCategorySerializer, RoleSerializer, UserAddressListSerializer, UserRolesListSerializer, \
    RefreshTokenSerializer, UserProfileInfoSerializer, UserProfileUpdateSerializer, UserRoleCreateSerializer, \
    UserAddressCreateSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts.filters import RoleFilter
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.files.models import Asset



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

        can_send, remaining_time = OtpCode.can_send_new_otp(mobile_number)
        if not can_send:
            return Response({
                "code_error": "otp_already_sent",
                'message': 'OTP already sent. Please wait before requesting again.',
                'remaining_time': remaining_time,
            }, status=status.HTTP_400_BAD_REQUEST)

        user.create_and_send_otp()
        return Response({'message': 'OTP_CodeSentSuccessfully', 'remaining_time': 120}, status=status.HTTP_200_OK)


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
        page = self.paginate_queryset(role_categories)
        serializer = self.get_serializer(role_categories, many=True)
        return self.get_paginated_response(serializer.data)



class RoleListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoleFilter

    serializer_class = RoleSerializer

    def get(self, request):
        roles = self.filter_queryset(Role.objects.all())
        page = self.paginate_queryset(roles)
        serializer = self.get_serializer(roles, many=True)
        return self.get_paginated_response(serializer.data)



class UserAddressListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAddressListSerializer

    def get(self, request):
        user_addresses = UserAddress.objects.filter(user=request.user)
        page = self.paginate_queryset(user_addresses)
        serializer = self.get_serializer(user_addresses, many=True)
        return self.get_paginated_response(serializer.data)


class UserAddressDetailApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAddressListSerializer

    def get(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk, user=request.user)
        serializer = self.get_serializer(user_address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressCreateApiview(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAddressCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_address = UserAddress(
            province=serializer.validated_data.get('province'),
            city=serializer.validated_data.get('city'),
            lat=serializer.validated_data.get('lat', None),
            lng=serializer.validated_data.get('lng', None),
            full_address=serializer.validated_data.get('full_address', None),
            postal_code=serializer.validated_data.get('postal_code', None),
            user=request.user
        )
        user_address.save()
        return Response({'message': 'AddressCreatedSuccessfully'}, status=status.HTTP_201_CREATED)


class UserAddressUpdateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserAddressCreateSerializer

    def put(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk, user=request.user)
        serializer = self.get_serializer(user_address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'AddressUpdatedSuccessfully'}, status=status.HTTP_200_OK)


class UserAddressDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk, user=request.user)
        user_address.delete()
        return Response({'message': 'AddressDeletedSuccessfully'}, status=status.HTTP_200_OK)


class UserRolesListApiView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserRolesListSerializer

    def get(self, request):
        user_roles = request.user.user_roles.all()
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRoleCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserRoleCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.validated_data['role']
        if UserRole.objects.filter(user=request.user, role=role).exists():
            return Response({'message': 'RoleAlreadyExists'}, status=status.HTTP_400_BAD_REQUEST)
        UserRole.objects.create(user=request.user, role=role)
        return Response({'message': 'RoleCreatedSuccessfully'}, status=status.HTTP_201_CREATED)


class UserRoleDetailApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserRolesListSerializer

    def get(self, request, pk):
        user_role = get_object_or_404(UserRole, pk=pk, user=request.user)
        serializer = self.get_serializer(user_role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRoleDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        user_role = get_object_or_404(UserRole, pk=pk, user=request.user)
        user_role.delete()
        return Response({'message': 'RoleDeletedSuccessfully'}, status=status.HTTP_200_OK)


class RefreshTokenApiView(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'InvalidOrExpiredRefreshToken'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileInfoApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProfileInfoSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProfileUpdateSerializer

    def put(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name', user.first_name)
            last_name = serializer.validated_data.get('last_name', user.last_name)
            image = serializer.validated_data.get('image', None)
            if image:
                if user.profile_image:
                    user.profile_image.delete()

                asset = Asset.objects.create(owner=user, image=image)
                user.profile_image = asset

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return Response(
                {"message": "ProfileUpdated"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

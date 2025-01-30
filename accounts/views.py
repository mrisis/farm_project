from django.template.defaultfilters import first
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OtpCode, RoleCategory, Role
from core.utils import send_sms_otp_code
from core.utils import generate_otp_code
from .serializers import SendOtpCodeSerializer, VerifyOtpCodeSerializer, UserSignupSerializer, RoleCategorySerializer, RoleSerializer
from django.shortcuts import get_object_or_404


class SendOtpApiView(GenericAPIView):
    serializer_class = SendOtpCodeSerializer

    def post(self,request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        user = get_object_or_404(User, mobile_number=mobile_number)
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

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        user = User.objects.create(mobile_number=mobile_number, first_name=first_name, last_name=last_name)
        user.create_and_send_otp()
        return Response({'message': 'UserCreatedSuccessfully'}, status=status.HTTP_201_CREATED)


class RoleCategoryCreateApiView(GenericAPIView):
    serializer_class = RoleCategorySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoleCategoryDetailApiView(GenericAPIView):
    serializer_class = RoleCategorySerializer
    def get(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        serializer = self.get_serializer(role_category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleCategoryListApiView(GenericAPIView):
    serializer_class = RoleCategorySerializer
    def get(self, request):
        role_categories = RoleCategory.objects.all()
        serializer = self.get_serializer(role_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleCategoryUpdateApiView(GenericAPIView):
    serializer_class = RoleCategorySerializer
    def put(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        serializer = self.get_serializer(role_category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleCategoryDeleteApiView(APIView):
    def delete(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        role_category.delete()
        return Response({'message': 'RoleCategoryDeletedSuccessfully'}, status=status.HTTP_204_NO_CONTENT)



class RoleCreateApiView(GenericAPIView):
    serializer_class = RoleSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoleDetailApiView(GenericAPIView):
    serializer_class = RoleSerializer
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = self.get_serializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleListApiView(GenericAPIView):
    serializer_class = RoleSerializer
    def get(self, request):
        roles = Role.objects.all()
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleUpdateApiView(GenericAPIView):
    serializer_class = RoleSerializer
    def put(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = self.get_serializer(role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleDeleteApiView(APIView):
    def delete(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return Response({'message': 'RoleDeletedSuccessfully'}, status=status.HTTP_204_NO_CONTENT)

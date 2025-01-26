from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OtpCode
from core.utils import send_sms_otp_code
from core.utils import generate_otp_code
from .serializers import SendOtpCodeSerializer, VerifyOtpCodeSerializer, UserSignupSerializer
from django.shortcuts import get_object_or_404


class SendOtpApiView(GenericAPIView):
    serializer_class = SendOtpCodeSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp_code = generate_otp_code()
            try:
                user = get_object_or_404(User, mobile_number=mobile_number)
                send_sms_otp_code(mobile_number, otp_code)
                OtpCode.objects.create(mobile_number=mobile_number, otp_code=otp_code)
                return Response({'message': 'OTP code sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOtpApiView(GenericAPIView):
    serializer_class = VerifyOtpCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp_code = serializer.validated_data['otp_code']
            try:
                otp = OtpCode.objects.filter(mobile_number=mobile_number, otp_code=otp_code, is_verified=False).first()
            except OtpCode.DoesNotExist:
                return Response({'message': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

            if not otp.is_valid() and not otp.is_verified:
                return Response({'message': 'OTP is expired'}, status=status.HTTP_400_BAD_REQUEST)

            if otp.otp_code != otp_code:
                return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(mobile_number=mobile_number)

            otp.is_verified = True
            otp.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'message': 'OTP verified successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignupApiView(GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        user = User.objects.create(mobile_number=mobile_number)
        if user:
            otp_code = generate_otp_code()
            send_sms_otp_code(mobile_number, otp_code)
            OtpCode.objects.create(mobile_number=mobile_number, otp_code=otp_code)
            return Response({'message': 'User created successfully & send Otp code'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)







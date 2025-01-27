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
        user = User.objects.create(mobile_number=mobile_number)
        user.create_and_send_otp()
        return Response({'message': 'UserCreatedSuccessfully'}, status=status.HTTP_201_CREATED)








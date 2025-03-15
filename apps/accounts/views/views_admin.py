from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers.serializers_admin import AdminLoginSerializer, UserListAdminSerializer
from apps.accounts.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

# class AdminLoginView(GenericAPIView):
#     serializer_class = AdminLoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.get(mobile_number=serializer.validated_data.get('mobile_number'))

#         if not user.is_admin:
#             return Response({'error': 'User is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

#         if not user.check_password(serializer.validated_data.get('password')):
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             access_token = RefreshToken.for_user(user).access_token
#             refresh_token = RefreshToken.for_user(user)
#             return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)}, status=status.HTTP_200_OK)
            
    




class AdminLoginView(GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        mobile_number = serializer.validated_data.get('mobile_number')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(mobile_number=mobile_number)
            if not user.is_admin:
                return Response({'error': 'User is not an admin'}, status=status.HTTP_403_FORBIDDEN)
            
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                'user': {
                    'id': user.id,
                    'mobile_number': user.mobile_number,
                    'is_admin': user.is_admin
                }
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        

class UserListAdminView(GenericAPIView):
    serializer_class = UserListAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers.serializers_admin import AdminLoginSerializer, UserListAdminSerializer, UserDetailAdminSerializer
from apps.accounts.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.accounts.filters import UserFilterAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404



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
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilterAdmin
    search_fields = ['mobile_number', 'first_name', 'last_name', 'user_roles__role__name']

    def get(self, request):
        users = User.objects.all()
        filtered_users = self.filter_queryset(users)
        serializer = self.serializer_class(filtered_users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class UserDetailAdminView(GenericAPIView):
    serializer_class = UserDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
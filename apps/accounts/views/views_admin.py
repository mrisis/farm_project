from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers.serializers_admin import AdminLoginSerializer, UserListAdminSerializer, UserDetailAdminSerializer, UserUpdateAdminSerializer, UserCreateAdminSerializer, RoleCategoryListAdminSerializer, RoleCategoryDetailAdminSerializer, RoleCategoryCreateAdminSerializer, RoleCategoryUpdateAdminSerializer, RoleListAdminSerializer, RoleDetailAdminSerializer, RoleCreateAdminSerializer, RoleUpdateAdminSerializer
from apps.accounts.models import User, RoleCategory,Role
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.accounts.filters import UserFilterAdmin, RoleFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from apps.files.models import Asset
from django.db import transaction


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
        

class UserCountAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count_of_users = User.objects.count()
        return Response({'count_of_users': count_of_users}, status=status.HTTP_200_OK)


class UserDetailAdminView(GenericAPIView):
    serializer_class = UserDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserUpdateAdminView(GenericAPIView):
    serializer_class = UserUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request,pk):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            image = serializer.validated_data.get('image', None)
            if image:
                if user.profile_image:
                    user.profile_image.delete()
                asset = Asset.objects.create(owner=user, image=image)
                user.profile_image = asset
            user.first_name = serializer.validated_data.get('first_name', user.first_name)
            user.last_name = serializer.validated_data.get('last_name', user.last_name)
            user.email = serializer.validated_data.get('email', user.email)
            user.mobile_number = serializer.validated_data.get('mobile_number', user.mobile_number)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                



class UserCreateAdminView(GenericAPIView):
    serializer_class = UserCreateAdminSerializer
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        confirm_password = validated_data.pop('confirm_password')

        image = validated_data.pop('image', None)

        user = User(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            mobile_number=validated_data.get('mobile_number'),

        )
        
        user.set_password(validated_data.get('password'))
        user.save()

        if image:
            asset = Asset.objects.create(owner=user, image=image)
            user.profile_image = asset
            user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        

class UserDeleteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(message='User deleted successfully', status=status.HTTP_200_OK)
    



class RoleCategoryListAdminView(GenericAPIView):
    serializer_class = RoleCategoryListAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        role_categories = RoleCategory.objects.all()
        serializer = self.serializer_class(role_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleCategoryDetailAdminView(GenericAPIView):
    serializer_class = RoleCategoryDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        serializer = self.serializer_class(role_category)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RoleCategoryCreateAdminView(GenericAPIView):
    serializer_class = RoleCategoryCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_category = RoleCategory(
            name=serializer.validated_data.get('name'),
            description=serializer.validated_data.get('description'),
        )
        role_category.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class RoleCategoryUpdateAdminView(GenericAPIView):
    serializer_class = RoleCategoryUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        serializer = self.serializer_class(role_category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RoleCategoryDeleteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        role_category = get_object_or_404(RoleCategory, pk=pk)
        role_category.delete()
        return Response({'message': 'Role category deleted successfully'}, status=status.HTTP_200_OK)
    



class RoleListAdminView(GenericAPIView):
    serializer_class = RoleListAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoleFilter
    search_fields = ['name', 'category__name']

    def get(self, request):
        roles = Role.objects.all()
        filtered_roles = self.filter_queryset(roles)
        serializer = self.serializer_class(filtered_roles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    



class RoleDetailAdminView(GenericAPIView):
    serializer_class = RoleDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = self.serializer_class(role, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class RoleCreateAdminView(GenericAPIView):
    serializer_class = RoleCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = Role(
            name=serializer.validated_data.get('name'),
            description=serializer.validated_data.get('description'),
            category=serializer.validated_data.get('category'),
            icon=serializer.validated_data.get('icon'),
        )
        role.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class RoleUpdateAdminView(GenericAPIView):
    serializer_class = RoleUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = self.serializer_class(role, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class RoleDeleteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return Response({'message': 'Role deleted successfully'}, status=status.HTTP_200_OK)
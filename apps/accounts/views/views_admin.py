from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers.serializers_admin import AdminLoginSerializer, UserListAdminSerializer, UserDetailAdminSerializer, UserUpdateAdminSerializer, UserCreateAdminSerializer, RoleCategoryListAdminSerializer, RoleCategoryDetailAdminSerializer, RoleCategoryCreateAdminSerializer, RoleCategoryUpdateAdminSerializer, RoleListAdminSerializer, RoleDetailAdminSerializer, RoleCreateAdminSerializer, RoleUpdateAdminSerializer, UserAddressListAdminSerializer, UserAddressDetailAdminSerializer, UserAddressCreateAdminSerializer, UserAddressUpdateAdminSerializer, OtpCodeListAdminSerializer, UserRoleListAdminSerializer, UserRoleDetailAdminSerializer, UserRoleCreateAdminSerializer, UserRoleUpdateAdminSerializer
from apps.accounts.models import User, RoleCategory,Role, UserAddress, OtpCode, UserRole
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.C_drf.C_paginations import CustomPageNumberPagination
from apps.accounts.filters import UserFilterAdmin, RoleFilter, UserAddressFilterAdmin, UserRoleFilterAdmin
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
        users_qs = self.filter_queryset(users)
        page = self.paginate_queryset(users_qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

        
        

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
    


class UserAddressListAdminView(GenericAPIView):
    serializer_class = UserAddressListAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserAddressFilterAdmin
    search_fields = ['user__mobile_number', 'province__name', 'city__name']

    def get(self, request):
        user_addresses = UserAddress.objects.all()
        filtered_user_addresses = self.filter_queryset(user_addresses)
        serializer = self.serializer_class(filtered_user_addresses, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class UserAddressDetailAdminView(GenericAPIView):
    serializer_class = UserAddressDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk)
        serializer = self.serializer_class(user_address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class UserAddressCreateAdminView(GenericAPIView):
    serializer_class = UserAddressCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_address = UserAddress(
            user=serializer.validated_data.get('user'),
            full_address=serializer.validated_data.get('full_address'),
            lat=serializer.validated_data.get('lat'),
            lng=serializer.validated_data.get('lng'),
            province=serializer.validated_data.get('province'),
            city=serializer.validated_data.get('city'),
        )
        user_address.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserAddressUpdateAdminView(GenericAPIView):
    serializer_class = UserAddressUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk)
        serializer = self.serializer_class(user_address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressDeleteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user_address = get_object_or_404(UserAddress, pk=pk)
        user_address.delete()
        return Response({'message': 'User address deleted successfully'}, status=status.HTTP_200_OK)
    



class OtpCodeListAdminView(GenericAPIView):
    serializer_class = OtpCodeListAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        otp_codes = OtpCode.objects.all()
        serializer = self.serializer_class(otp_codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class UserRoleListAdminView(GenericAPIView):
    serializer_class = UserRoleListAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserRoleFilterAdmin
    search_fields = ['user__mobile_number', 'role__name', 'user__first_name', 'user__last_name']


    def get(self, request):
        user_roles = UserRole.objects.all()
        filtered_user_roles = self.filter_queryset(user_roles)
        serializer = self.serializer_class(filtered_user_roles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class UserRoleDetailAdminView(GenericAPIView):
    serializer_class = UserRoleDetailAdminSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user_role = get_object_or_404(UserRole, pk=pk)
        serializer = self.serializer_class(user_role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class UserRoleCreateAdminView(GenericAPIView):
    serializer_class = UserRoleCreateAdminSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_role = UserRole(
            user=serializer.validated_data.get('user'),
            role=serializer.validated_data.get('role'),
        )
        user_role.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class UserRoleUpdateAdminView(GenericAPIView):
    serializer_class = UserRoleUpdateAdminSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user_role = get_object_or_404(UserRole, pk=pk)
        serializer = self.serializer_class(user_role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserRoleDeleteAdminView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user_role = get_object_or_404(UserRole, pk=pk)
        user_role.delete()
        return Response({'message': 'User role deleted successfully'}, status=status.HTTP_200_OK)
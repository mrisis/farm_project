from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OtpCode, RoleCategory, Role, UserAddress, UserRole
from .forms import UserCreationForm,UserchangeForm

class UserAdmin(BaseUserAdmin):
    form = UserchangeForm
    add_form = UserCreationForm
    list_display = ['id','mobile_number','first_name','last_name','is_admin', 'is_active']
    list_filter = ('is_admin',)
    fieldsets = (
        (None,{'fields':('mobile_number','password')}),
        ('permission',{'fields':('is_admin','groups','user_permissions','is_superuser')}),
    )

    add_fieldsets = (
        (None,{'fields':('mobile_number','email','password1','password2')}),
    )

    search_fields = ['mobile_number',]
    ordering = ('first_name',)
    filter_horizontal = ('groups','user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request,obj,**kwargs)
        is_superuser=request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled=True
        return form

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id','user','province','city','full_address','postal_code']
    search_fields = ['user','province','city','full_address','postal_code']
    list_filter = ('province','city', 'user')


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['id','mobile_number','otp_code','is_verified']
    list_filter = ('is_verified',)
    search_fields = ['mobile_number','otp_code']


class RoleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']
    search_fields = ['name','description']
    list_filter = ('name',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id','name','description', 'category', 'category_id']
    search_fields = ['name','description', 'category',]
    list_filter = ('name', 'category')

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id','user','role']
    search_fields = ['user__mobile_number','role__name']
    list_filter = ('user', 'role', 'user__mobile_number')



admin.site.register(User,UserAdmin)
admin.site.register(OtpCode,OtpCodeAdmin)
admin.site.register(RoleCategory,RoleCategoryAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserRole, UserRoleAdmin)
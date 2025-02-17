from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.timezone import now
from datetime import timedelta
from core.models import BaseUserModel, BaseModel
from core.utils import generic_funcs
from apps.locations.models import Province, City


class User(AbstractBaseUser, BaseUserModel, PermissionsMixin):

    class GenderChoice(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderChoice.choices, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.OneToOneField(
        'files.Asset',
        on_delete=models.SET_NULL,
        related_name='user_profile_image',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'mobile_number'
    objects = UserManager()

    def __str__(self):
        return self.mobile_number

    def create_and_send_otp(self):
        otp_code = generic_funcs.generate_otp_code()
        print(otp_code)
        generic_funcs.send_sms_otp_code(self.mobile_number, otp_code)
        OtpCode.objects.create(mobile_number=self.mobile_number, otp_code=otp_code)






    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class UserAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='addresses')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')
    lat = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.user.mobile_number} - {self.full_address}'


class OtpCode(BaseModel):
    mobile_number = models.CharField(max_length=11)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.mobile_number} - {self.otp_code}'

    def is_valid(self):
        return now() < self.created_at + timedelta(seconds=80)

    def verify_otp_code(self, provided_otp):
        if not self.is_valid():
            return False
        if self.otp_code != provided_otp:
            return False
        self.is_verified = True
        self.save()
        return True

    @classmethod
    def can_send_new_otp(cls, mobile_number, wait_minutes=2):

        last_otp = cls.objects.filter(mobile_number=mobile_number).order_by('-created_at').first()
        if last_otp:
            valid_until = last_otp.created_at + timedelta(minutes=wait_minutes)
            if now() < valid_until:
                remaining_time = int((valid_until - now()).total_seconds())
                return False, remaining_time
        return True, timedelta(minutes=wait_minutes).total_seconds()


class RoleCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Role(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(RoleCategory, on_delete=models.CASCADE, related_name='roles')
    icon = models.FileField(
        upload_to='roles/icons/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        unique_together = (("user", "role"),)

    def __str__(self):
        return f'{self.user.mobile_number} - {self.role.name}'


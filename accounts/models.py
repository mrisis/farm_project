from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . managers import UserManager
from core.models import BaseUserModel

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

    USERNAME_FIELD = 'mobile_number'
    objects = UserManager()

    def __str__(self):
        return self.mobile_number





    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



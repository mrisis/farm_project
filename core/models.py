from django.db import models
from django.utils import timezone
from .managers import BaseManager
from django.conf import settings


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="Deleted Datetime",
        help_text="This is deleted datetime"
    )


    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,
        verbose_name="Deleted status",
        help_text="This is deleted status",
    )

    is_active = models.BooleanField(
        default=True,
        editable=False,
        verbose_name="Active status",
        help_text="This is active status",
    )



    def deleter(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save(using=using)


    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()


class BaseUserModel(BaseModel):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_users",

    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_users",

    )

    class Meta:
        abstract = True
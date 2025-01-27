from django.db import models
from core.models import BaseModel
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Asset(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assets')
    file = models.FileField(upload_to='files/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        owner_mobile_number = self.owner.mobile_number if self.owner else 'بدون مالک'
        return f'{self.id} - {owner_mobile_number}'





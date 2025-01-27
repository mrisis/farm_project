from django.db import models
from core.models import BaseModel
from accounts.models import User



class Asset(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assets')
    file = models.FileField(upload_to='files/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.id}'





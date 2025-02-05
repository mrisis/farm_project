from django.db import models
from core.models import BaseModel


class Province(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class City(BaseModel):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
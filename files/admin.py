from django.contrib import admin
from .models import Asset


class AssetAdmin(admin.ModelAdmin):
    list_display = ['id','owner', 'file', 'image']
    search_fields = ['owner', 'file', 'image']
    list_filter = ['owner', 'file', 'image']


admin.site.register(Asset, AssetAdmin)







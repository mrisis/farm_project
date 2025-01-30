from django.contrib import admin
from .models import Province


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


admin.site.register(Province, ProvinceAdmin)

from django.contrib import admin
from .models import Province, City


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'province')
    list_filter = ('province__name',)
    search_fields = ('name', 'province__name')
    ordering = ('name',)


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)


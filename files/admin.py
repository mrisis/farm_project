from django.contrib import admin
from .models import Asset
from django.utils.html import format_html



class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_file', 'owner', 'get_content_object', 'created_at')
    list_filter = ('owner', 'content_type', 'created_at')
    search_fields = ('id', 'owner__mobile_number')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def display_file(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)
    display_file.short_description = 'فایل/تصویر'

    def get_content_object(self, obj):
        if obj.content_object:
            return f"{obj.content_type} - ID: {obj.object_id}"
        return "-"

    get_content_object.short_description = 'محتوای مرتبط'

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('owner', 'file', 'image')
        }),
        ('ارتباطات', {
            'fields': ('content_type', 'object_id'),
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


admin.site.register(Asset, AssetAdmin)





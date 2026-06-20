from django.contrib import admin
from .models import (
     Resource, Honor, AboutInfo, GalleryItem, SocialLink
)

# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ['title', 'category', 'created_at']
#     search_fields = ['title', 'category']
#     list_filter = ['category']

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['title', 'date_jalali', 'time', 'is_upcoming']
#     list_filter = ['is_upcoming']
#     search_fields = ['title']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'download_count']
    search_fields = ['title']

@admin.register(Honor)
class HonorAdmin(admin.ModelAdmin):
    list_display = ['competition_name', 'rank', 'order']
    list_editable = ['order']
    search_fields = ['competition_name']

@admin.register(AboutInfo)
class AboutInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('متن درباره ما', {
            'fields': ('description',)
        }),
        ('آمارها', {
            'fields': ('active_members', 'events_held', 'total_resources')
        }),
    )

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['caption_title', 'media_type', 'order']
    list_editable = ['order']
    list_filter = ['media_type']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'is_footer', 'is_floating', 'order']
    list_editable = ['is_footer', 'is_floating', 'order']
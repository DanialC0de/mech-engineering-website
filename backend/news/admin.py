from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'jalali_date', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'summary', 'content')
    ordering = ('-created_at',)
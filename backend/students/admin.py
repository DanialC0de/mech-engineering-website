# students/admin.py
from django.contrib import admin
from .models import StudentProfile
from .models import StudentProfile


class StudentProfileAdmin(admin.ModelAdmin):
    """ادمین برای پروفایل دانشجویان"""
    
    list_display = ('user', 'student_id', 'major', 'level', 'entry_year', 'created_at')
    list_filter = ('level', 'major', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id', 'major')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('student_id', 'major', 'level', 'entry_year')
        }),
        ('عکس پروفایل', {
            'fields': ('avatar',)
        }),
        ('تنظیمات', {
            'fields': ('receive_notifications',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ثبت در ادمین
admin.site.register(StudentProfile, StudentProfileAdmin)
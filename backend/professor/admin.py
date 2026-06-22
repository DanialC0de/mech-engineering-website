# professor/admin.py
from django.contrib import admin
from .models import ProfessorProfile, EventInvitation


class ProfessorProfileAdmin(admin.ModelAdmin):
    """ادمین برای پروفایل اساتید"""
    
    list_display = ('user', 'employee_id', 'academic_rank', 'department', 'created_at')
    list_filter = ('academic_rank', 'department', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id', 'field_of_study')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات شغلی', {
            'fields': ('employee_id', 'department', 'academic_rank', 'field_of_study', 'office_number')
        }),
        ('اطلاعات پژوهشی', {
            'fields': ('research_interests', 'publications', 'bio')
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


@admin.register(EventInvitation)
class EventInvitationAdmin(admin.ModelAdmin):
    """ادمین برای دعوتنامه‌های رویداد"""
    
    list_display = ('professor', 'event', 'role', 'status', 'created_at')
    list_filter = ('status', 'role', 'created_at')
    search_fields = ('professor__username', 'professor__first_name', 'professor__last_name', 'event__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('status',)
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('event', 'professor', 'role', 'status')
        }),
        ('پیام', {
            'fields': ('message',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['accept_invitations', 'decline_invitations']
    
    def accept_invitations(self, request, queryset):
        count = queryset.update(status='accepted')
        self.message_user(request, f"{count} دعوتنامه پذیرفته شد.")
    accept_invitations.short_description = "پذیرفتن دعوتنامه‌های انتخاب شده"
    
    def decline_invitations(self, request, queryset):
        count = queryset.update(status='declined')
        self.message_user(request, f"{count} دعوتنامه رد شد.")
    decline_invitations.short_description = "رد کردن دعوتنامه‌های انتخاب شده"


# ثبت در ادمین
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)

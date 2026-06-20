from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'jalali_date', 'time', 'status', 'capacity', 'registered_count')
    list_filter = ('status', 'is_full')
    search_fields = ('title',)  # ← فقط عنوان
    readonly_fields = ('registered_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('status',)
    list_per_page = 20
    
    actions = ['change_status_to_upcoming', 'change_status_to_completed']
    
    def change_status_to_upcoming(self, request, queryset):
        queryset.update(status='upcoming')
        self.message_user(request, f"{queryset.count()} رویداد به 'در حال ثبت‌نام' تغییر یافت.")
    change_status_to_upcoming.short_description = "تغییر به 'در حال ثبت‌نام'"
    
    def change_status_to_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} رویداد به 'پایان‌یافته' تغییر یافت.")
    change_status_to_completed.short_description = "تغییر به 'پایان‌یافته'"


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registered_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('registered_at',)
    ordering = ('-registered_at',)
    list_editable = ('status',)
    list_per_page = 20
    
    actions = ['confirm', 'cancel']
    
    def confirm(self, request, queryset):
        count = queryset.update(status='confirmed')
        self.message_user(request, f"{count} ثبت‌نام تأیید شد.")
    confirm.short_description = "تأیید ثبت‌نام"
    
    def cancel(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f"{count} ثبت‌نام لغو شد.")
    cancel.short_description = "لغو ثبت‌نام"
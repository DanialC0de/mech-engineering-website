# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    """ادمین سفارشی برای مدل CustomUser"""
    
    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'get_role_display', 'is_phone_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_phone_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'phone_number', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('نقش و دسترسی‌ها', {'fields': ('role', 'is_phone_verified')}),
        ('مجوزها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2', 'role'),
        }),
    )
    
    def get_role_display(self, obj):
        """نمایش فارسی نقش کاربر"""
        return dict(CustomUser.ROLE_CHOICES).get(obj.role, obj.role)
    get_role_display.short_description = "نقش کاربر"


# ============================================
# ✅ کلاس OTPAdmin را تعریف کنید
# ============================================
class OTPAdmin(admin.ModelAdmin):
    """ادمین برای کدهای تایید"""
    list_display = ('phone_number', 'code', 'created_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number', 'code')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = "منقضی شده"


# ثبت در ادمین
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
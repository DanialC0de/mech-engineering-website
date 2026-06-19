from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """پنل مدیریت رویدادها"""
    
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('title', 'jalali_date', 'time', 'status', 'capacity', 'registered_count', 'is_full', 'created_at')
    
    # فیلترها
    list_filter = ('status', 'is_full', 'created_at', 'updated_at')
    
    # فیلدهای جستجو
    search_fields = ('title', 'short_description', 'full_description', 'instructor_name')
    
    # فیلدهای فقط خواندنی
    readonly_fields = ('registered_count', 'created_at', 'updated_at')
    
    # مرتب‌سازی پیش‌فرض
    ordering = ('-created_at',)
    
    # فیلدهایی که قابل ویرایش در لیست هستند
    list_editable = ('status', 'is_full')
    
    # تعداد آیتم در هر صفحه
    list_per_page = 20
    
    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'image', 'short_description', 'full_description')
        }),
        ('سرفصل‌ها و مدرس', {
            'fields': ('syllabus', 'instructor_name', 'instructor_title', 'instructor_image'),
            'classes': ('collapse',),
        }),
        ('زمان برگزاری', {
            'fields': ('jalali_date', 'time', 'start_datetime'),
        }),
        ('ظرفیت و وضعیت', {
            'fields': ('status', 'capacity', 'registered_count', 'is_full'),
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # اکشن‌های سفارشی
    actions = ['mark_as_upcoming', 'mark_as_ongoing', 'mark_as_completed', 'reset_registrations']
    
    def mark_as_upcoming(self, request, queryset):
        """تغییر وضعیت به آینده"""
        queryset.update(status='upcoming')
        self.message_user(request, f"{queryset.count()} رویداد به وضعیت 'در حال ثبت‌نام' تغییر یافت.")
    mark_as_upcoming.short_description = "تغییر وضعیت به 'در حال ثبت‌نام'"
    
    def mark_as_ongoing(self, request, queryset):
        """تغییر وضعیت به در حال برگزاری"""
        queryset.update(status='ongoing')
        self.message_user(request, f"{queryset.count()} رویداد به وضعیت 'در حال برگزاری' تغییر یافت.")
    mark_as_ongoing.short_description = "تغییر وضعیت به 'در حال برگزاری'"
    
    def mark_as_completed(self, request, queryset):
        """تغییر وضعیت به پایان رسیده"""
        queryset.update(status='completed', is_full=True)
        self.message_user(request, f"{queryset.count()} رویداد به وضعیت 'به پایان رسیده' تغییر یافت.")
    mark_as_completed.short_description = "تغییر وضعیت به 'به پایان رسیده'"
    
    def reset_registrations(self, request, queryset):
        """بازنشانی تعداد ثبت‌نام‌ها"""
        for event in queryset:
            event.registered_count = 0
            event.is_full = False
            event.save(update_fields=['registered_count', 'is_full'])
        self.message_user(request, f"تعداد ثبت‌نام‌های {queryset.count()} رویداد بازنشانی شد.")
    reset_registrations.short_description = "بازنشانی تعداد ثبت‌نام‌ها"


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """پنل مدیریت ثبت‌نام‌ها"""
    
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('user', 'event', 'status', 'registered_at', 'get_user_full_name')
    
    # فیلترها
    list_filter = ('status', 'registered_at', 'event__status')
    
    # فیلدهای جستجو
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'event__title')
    
    # فیلدهای فقط خواندنی
    readonly_fields = ('registered_at',)
    
    # مرتب‌سازی پیش‌فرض
    ordering = ('-registered_at',)
    
    # فیلدهایی که قابل ویرایش در لیست هستند
    list_editable = ('status',)
    
    # تعداد آیتم در هر صفحه
    list_per_page = 20
    
    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات ثبت‌نام', {
            'fields': ('event', 'user', 'status')
        }),
        ('زمان', {
            'fields': ('registered_at',),
            'classes': ('collapse',),
        }),
    )
    
    # اکشن‌های سفارشی
    actions = ['confirm_registrations', 'cancel_registrations', 'mark_attended']
    
    def get_user_full_name(self, obj):
        """نمایش نام کامل کاربر"""
        return obj.user.get_full_name() or obj.user.username
    get_user_full_name.short_description = "نام کاربر"
    
    def confirm_registrations(self, request, queryset):
        """تأیید ثبت‌نام‌ها"""
        count = 0
        for registration in queryset:
            if registration.status == 'pending':
                registration.status = 'confirmed'
                registration.save()
                registration.event.update_registration_count()
                count += 1
        self.message_user(request, f"{count} ثبت‌نام تأیید شد.")
    confirm_registrations.short_description = "تأیید ثبت‌نام‌های انتخاب‌شده"
    
    def cancel_registrations(self, request, queryset):
        """لغو ثبت‌نام‌ها"""
        count = 0
        for registration in queryset:
            if registration.status != 'cancelled':
                registration.status = 'cancelled'
                registration.save()
                registration.event.update_registration_count()
                count += 1
        self.message_user(request, f"{count} ثبت‌نام لغو شد.")
    cancel_registrations.short_description = "لغو ثبت‌نام‌های انتخاب‌شده"
    
    def mark_attended(self, request, queryset):
        """علامت‌گذاری به عنوان حضور یافته"""
        count = 0
        for registration in queryset:
            if registration.status == 'confirmed':
                registration.attended = True
                registration.save()
                count += 1
        self.message_user(request, f"{count} ثبت‌نام به عنوان 'حضور یافته' علامت‌گذاری شد.")
    mark_attended.short_description = "علامت‌گذاری به عنوان 'حضور یافته'"
    
    # محدودیت‌ها
    def get_queryset(self, request):
        """بهینه‌سازی کوئری با select_related"""
        return super().get_queryset(request).select_related('user', 'event')
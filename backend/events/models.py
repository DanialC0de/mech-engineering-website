from django.db import models
from django.conf import settings
from django.utils import timezone
class Event(models.Model):
    """مدل رویدادها و کارگاه‌ها"""
    
    STATUS_CHOICES = (
        ('upcoming', 'در حال ثبت‌نام'),
        ('ongoing', 'در حال برگزاری'),
        ('completed', 'به پایان رسیده'),
    )
    
    # فیلدهای اصلی
    title = models.CharField(max_length=200, verbose_name="عنوان رویداد")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="تصویر")
    short_description = models.TextField(verbose_name="توضیحات کوتاه")
    
    # ⭐ فیلدهای جدید برای صفحه جزئیات
    full_description = models.TextField(verbose_name="توضیحات کامل", blank=True)
    syllabus = models.TextField(verbose_name="سرفصل‌ها", blank=True, help_text="هر سرفصل در یک خط")
    
    # ⭐ اطلاعات مدرس
    instructor_name = models.CharField(max_length=100, verbose_name="نام مدرس", blank=True)
    instructor_title = models.CharField(max_length=100, verbose_name="عنوان مدرس", blank=True)
    instructor_image = models.ImageField(upload_to='instructors/', blank=True, null=True, verbose_name="تصویر مدرس")
    
    # زمان
    jalali_date = models.CharField(max_length=50,blank=True,
    null=True, verbose_name="تاریخ شمسی", help_text="مثال: ۱۴۰۴/۰۱/۲۰")
    time = models.CharField(max_length=20, verbose_name="ساعت", help_text="مثال: ۱۵:۰۰")
    
    # وضعیت و ظرفیت
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name="وضعیت")
    capacity = models.PositiveIntegerField(default=0, verbose_name="ظرفیت (۰=نامحدود)")
    registered_count = models.PositiveIntegerField(default=0, verbose_name="تعداد ثبت‌نام‌ها")
    is_full = models.BooleanField(default=False, verbose_name="تکمیل شده")
    
    # زمان ایجاد
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_full']),
        ]
    
    def __str__(self):
        return self.title
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events',
        verbose_name="ایجاد کننده"
    )

    @property
    def is_upcoming(self):
        """سازگاری با کدهای قبلی"""
        return self.status == 'upcoming'
    
    def can_register(self):
        """بررسی امکان ثبت‌نام"""
        return self.status == 'upcoming' and not self.is_full
    
    def update_registration_count(self):
        """به‌روزرسانی تعداد ثبت‌نام‌ها"""
        self.registered_count = self.registrations.filter(
            status__in=['pending', 'confirmed']
        ).count()
        
        if self.capacity > 0 and self.registered_count >= self.capacity:
            self.is_full = True
        else:
            self.is_full = False
            
        self.save(update_fields=['registered_count', 'is_full'])
    
    def save(self, *args, **kwargs):
        if self.capacity == 0:
            self.is_full = False
        super().save(*args, **kwargs)


class Registration(models.Model):
    """ثبت‌نام کاربر در رویداد"""
    
    STATUS_CHOICES = (
        ('pending', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('cancelled', 'لغو شده'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
        unique_together = ['event', 'user']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.event.title}"

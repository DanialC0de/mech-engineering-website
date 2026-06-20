# students/models.py
from django.db import models
from django.conf import settings
from events.models import Event, Registration
from news.models import News

class StudentProfile(models.Model):
    """تکمیل اطلاعات دانشجو"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    
    # فیلدهای اضافی
    student_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره دانشجویی")
    major = models.CharField(max_length=100, blank=True, null=True, verbose_name="رشته تحصیلی")
    level = models.CharField(max_length=50, blank=True, null=True, verbose_name="مقطع تحصیلی")
    entry_year = models.IntegerField(null=True, blank=True, verbose_name="سال ورود")
    
    # ========================================
    # ✅ فیلدهای جدید برای مطابقت با فرم ثبت‌نام
    # ========================================
    term = models.CharField(max_length=50, blank=True, null=True, verbose_name="ترم تحصیلی")
    committee = models.CharField(max_length=100, blank=True, null=True, verbose_name="کمیته مورد نظر")
    interest = models.CharField(max_length=200, blank=True, null=True, verbose_name="تخصص/علاقه‌مندی")
    bio = models.TextField(blank=True, null=True, verbose_name="درباره خود")
    
    # عکس پروفایل
    avatar = models.ImageField(
        upload_to='students/avatars/',
        default='students/avatars/default.png',
        blank=True,
        null=True,
        verbose_name="عکس پروفایل"
    )
    
    # تنظیمات
    receive_notifications = models.BooleanField(default=True, verbose_name="دریافت نوتیفیکیشن")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پروفایل دانشجو"
        verbose_name_plural = "پروفایل‌های دانشجویان"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"
    
    def get_full_name(self):
        return self.user.get_full_name() or self.user.username
    
    def get_event_count(self):
        """تعداد رویدادهای شرکت کرده"""
        return Registration.objects.filter(
            user=self.user,
            status='confirmed'
        ).count()
    
    def get_download_count(self):
        """تعداد دانلودهای منابع"""
        return 0
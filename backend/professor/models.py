# professor/models.py
from django.db import models
from django.conf import settings
from events.models import Event, Registration
from news.models import News

class ProfessorProfile(models.Model):
    """تکمیل اطلاعات استاد"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='professor_profile'
    )
    
    # فیلدهای اضافی
    employee_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره پرسنلی")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="دانشکده")
    academic_rank = models.CharField(max_length=50, blank=True, null=True, verbose_name="مرتبه علمی")
    field_of_study = models.CharField(max_length=100, blank=True, null=True, verbose_name="رشته تخصصی")
    
    # اطلاعات تماس و پژوهشی
    office_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="شماره دفتر")
    research_interests = models.TextField(blank=True, null=True, verbose_name="زمینه‌های پژوهشی")
    publications = models.TextField(blank=True, null=True, verbose_name="مقالات و تالیفات")
    bio = models.TextField(blank=True, null=True, verbose_name="درباره خود")
    
    # عکس پروفایل
    avatar = models.ImageField(
        upload_to='professors/avatars/',
        default='professors/avatars/default.png',
        blank=True,
        null=True,
        verbose_name="عکس پروفایل"
    )
    
    # تنظیمات
    receive_notifications = models.BooleanField(default=True, verbose_name="دریافت نوتیفیکیشن")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پروفایل استاد"
        verbose_name_plural = "پروفایل‌های اساتید"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    def get_full_name(self):
        return self.user.get_full_name() or self.user.username
    
    def get_event_count(self):
        """تعداد رویدادهایی که استاد مدرس آن است"""
        return Event.objects.filter(instructor_name__icontains=self.user.get_full_name()).count()
    
    def get_upcoming_events(self):
        """رویدادهای پیش رو که استاد مدرس آن است"""
        return Event.objects.filter(
            instructor_name__icontains=self.user.get_full_name(),
            status='upcoming'
        )


class EventInvitation(models.Model):
    """دعوتنامه برای استاد جهت تدریس یا سخنرانی در رویداد"""
    
    STATUS_CHOICES = (
        ('pending', 'در انتظار پاسخ'),
        ('accepted', 'پذیرفته شده'),
        ('declined', 'رد شده'),
    )
    
    ROLE_CHOICES = (
        ('instructor', 'مدرس'),
        ('speaker', 'سخنران'),
        ('moderator', 'مجری'),
        ('judge', 'داور'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='professor_invitations')
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='event_invitations'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='instructor', verbose_name="نقش")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    message = models.TextField(blank=True, null=True, verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "دعوتنامه رویداد"
        verbose_name_plural = "دعوتنامه‌های رویداد"
        unique_together = ['event', 'professor']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.event.title} ({self.get_role_display()})"

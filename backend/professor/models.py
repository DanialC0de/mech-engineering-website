from django.db import models
from django.conf import settings
from events.models import Event


class ProfessorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='professor_profile'
    )
    employee_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره پرسنلی")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="دانشکده")
    academic_rank = models.CharField(max_length=50, blank=True, null=True, verbose_name="مرتبه علمی")
    field_of_study = models.CharField(max_length=100, blank=True, null=True, verbose_name="رشته تخصصی")
    office_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="شماره دفتر")
    research_interests = models.TextField(blank=True, null=True, verbose_name="زمینه‌های پژوهشی")
    publications = models.TextField(blank=True, null=True, verbose_name="مقالات و تالیفات")
    bio = models.TextField(blank=True, null=True, verbose_name="درباره خود")
    avatar = models.ImageField(
        upload_to='professors/avatars/',
        default='professors/avatars/default.png',
        blank=True,
        null=True,
        verbose_name="عکس پروفایل"
    )
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
        return Event.objects.filter(instructor_name__icontains=self.user.get_full_name()).count()

    def get_upcoming_events(self):
        return Event.objects.filter(
            instructor_name__icontains=self.user.get_full_name(),
            status='upcoming'
        )


class EventInvitation(models.Model):
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


class ProfessorArticle(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('submitted', 'ارسال شده به دبیر انجمن'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    )

    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    abstract = models.TextField(verbose_name="چکیده مقاله")
    file = models.FileField(upload_to='professor_articles/', verbose_name="فایل مقاله (PDF)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")
    admin_feedback = models.TextField(blank=True, verbose_name="نظر دبیر انجمن")

    class Meta:
        verbose_name = "پیشنهاد مقاله"
        verbose_name_plural = "پیشنهادات مقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EventProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    )
    TYPE_CHOICES = (
        ('کارگاه', 'کارگاه'),
        ('سمینار', 'سمینار'),
        ('نشست علمی', 'نشست علمی'),
    )

    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_proposals'
    )
    title = models.CharField(max_length=200, verbose_name="عنوان پیشنهادی")
    description = models.TextField(verbose_name="توضیحات")
    proposed_date = models.CharField(max_length=50, verbose_name="تاریخ پیشنهادی", help_text="مثال: ۱۴۰۴/۰۲/۱۰")
    event_type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="نوع رویداد")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_feedback = models.TextField(blank=True, verbose_name="نظر دبیر")

    class Meta:
        verbose_name = "پیشنهاد رویداد"
        verbose_name_plural = "پیشنهادات رویداد"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.professor.get_full_name()}"
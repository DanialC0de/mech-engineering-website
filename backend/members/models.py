from django.db import models
from django.conf import settings

class Committee(models.Model):
    """کمیته‌های انجمن"""
    name = models.CharField(max_length=100, verbose_name="نام کمیته")
    
    class Meta:
        verbose_name = "کمیته"
        verbose_name_plural = "کمیته‌ها"
    
    def __str__(self):
        return self.name


class Member(models.Model):
    """اعضای انجمن"""
    
    ROLE_CHOICES = (
        ('head', 'رئیس'),
        ('vice', 'نائب رئیس'),
        ('secretary', 'دبیر'),
        ('committee_head', 'مسئول کمیته'),
        ('member', 'عضو'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='member_profile'
    )
    committee = models.ForeignKey(
        Committee, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    student_id = models.CharField(max_length=20, unique=True, verbose_name="شماره دانشجویی")
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "اعضا"
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

class GalleryImage(models.Model):
    """تصاویر گالری انجمن"""
    title = models.CharField(max_length=200, verbose_name="عنوان تصویر")
    image = models.ImageField(upload_to='gallery/', verbose_name="تصویر")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "تصاویر گالری"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title



class MemberRequest(models.Model):
    """درخواست عضویت"""
    
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('approved', 'تأیید شده'),
        ('rejected', 'رد شده'),
    )
    message = models.TextField(
    blank=True,
    null=True,
    verbose_name='پیام متقاضی'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membership_requests'
    )
    committee = models.ForeignKey(
        Committee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    student_id = models.CharField(
        max_length=20,
        unique=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):

        old_status = None

        if self.pk:
            try:
                old_status = MemberRequest.objects.get(pk=self.pk).status
            except MemberRequest.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if old_status != 'approved' and self.status == 'approved':

            Member.objects.get_or_create(
                user=self.user,
                defaults={
                    'committee': self.committee,
                    'student_id': self.student_id,
                    'role': 'member',
                    'is_active': True,
                })


    class Meta:
        verbose_name = "درخواست عضویت"
        verbose_name_plural = "درخواست‌های عضویت"
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"


class InternalResource(models.Model):
    """منابع داخلی"""
    
    CATEGORY_CHOICES = (
        ('educational', 'آموزشی'),
        ('administrative', 'اداری'),
        ('research', 'پژوهشی'),
        ('other', 'سایر'),
    )
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='educational')
    file = models.FileField(upload_to='members/resources/', blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_resources'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "منبع داخلی"
        verbose_name_plural = "منابع داخلی"
    
    def __str__(self):
        return self.title
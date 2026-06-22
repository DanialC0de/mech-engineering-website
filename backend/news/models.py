from django.db import models
from django.utils import timezone
import jdatetime
# از django.utils.text import slugify حذف شد چون نیازی نیست


class News(models.Model):
    """مدل اخبار و اطلاعیه‌ها"""

    CATEGORY_CHOICES = (
        ('announcement', 'اطلاعیه'),
        ('event', 'رویداد'),
        ('academic', 'آموزشی'),
        ('research', 'پژوهشی'),
        ('industry', 'صنعت'),
        ('other', 'سایر'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="تصویر")
    summary = models.TextField(verbose_name="خلاصه خبر", max_length=300,
                               help_text="متن کوتاه برای نمایش در کارت‌های خبر")
    content = models.TextField(verbose_name="متن کامل خبر")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,
                                default='announcement', verbose_name="دسته‌بندی")

    jalali_date = models.CharField(max_length=50, verbose_name="تاریخ شمسی")

    is_published = models.BooleanField(default=True, verbose_name="منتشر شود؟")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_category_display_fa(self):
        """نمایش فارسی دسته‌بندی برای HTML"""
        return dict(self.CATEGORY_CHOICES).get(self.category, 'سایر')

    def jalali_publish_date(self):
        """تاریخ شمسی برای نمایش"""
        return self.jalali_date

    def save(self, *args, **kwargs):
        # فقط ذخیره‌سازی ساده، بدون تولید slug
        super().save(*args, **kwargs)
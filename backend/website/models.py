from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    category = models.CharField(max_length=100, verbose_name="دسته‌بندی")
    summary = models.CharField(max_length=300, blank=True, verbose_name="خلاصه")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="تصویر")
    link = models.CharField(max_length=500, blank=True, verbose_name="لینک")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان رویداد")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="تصویر")
    date_jalali = models.CharField(max_length=50, verbose_name="تاریخ شمسی")
    time = models.CharField(max_length=20, verbose_name="ساعت")
    short_description = models.TextField(verbose_name="توضیحات کوتاه")
    is_upcoming = models.BooleanField(default=True, verbose_name="رویداد آینده")

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"
        ordering = ['date_jalali']

    def __str__(self):
        return self.title


# 3. مدل منابع علمی
class Resource(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان منبع")
    image = models.ImageField(upload_to='resources/', blank=True, null=True, verbose_name="تصویر")
    description = models.TextField(verbose_name="توضیحات")
    file = models.FileField(upload_to='resources/files/', blank=True, null=True, verbose_name="فایل")
    download_count = models.IntegerField(default=0, verbose_name="تعداد دانلود")

    class Meta:
        verbose_name = "منبع علمی"
        verbose_name_plural = "منابع علمی"

    def __str__(self):
        return self.title


# 4. مدل افتخارات (جدول)
class Honor(models.Model):
    competition_name = models.CharField(max_length=200, verbose_name="عنوان جشنواره یا مسابقه")
    rank = models.CharField(max_length=200, verbose_name="مقام")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "افتخار"
        verbose_name_plural = "افتخارات"
        ordering = ['order']

    def __str__(self):
        return f"{self.competition_name} - {self.rank}"


# 5. مدل درباره ما و آمار
class AboutInfo(models.Model):
    description = models.TextField(verbose_name="توضیحات درباره ما")
    active_members = models.IntegerField(default=0, verbose_name="تعداد اعضای فعال")
    events_held = models.IntegerField(default=0, verbose_name="تعداد رویدادهای برگزار شده")
    total_resources = models.IntegerField(default=0, verbose_name="تعداد منابع علمی")

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return "درباره انجمن علمی مکانیک"


# 6. مدل گالری تصاویر و ویدیوها (اسلایدر)
class GalleryItem(models.Model):
    TYPE_CHOICES = [
        ('image', 'تصویر'),
        ('video', 'ویدیو'),
    ]
    
    media_type = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name="نوع رسانه")
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True, verbose_name="تصویر")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, verbose_name="فایل ویدیو")
    caption_title = models.CharField(max_length=200, verbose_name="عنوان")
    caption_text = models.CharField(max_length=300, blank=True, verbose_name="متن پایین اسلاید")
    order = models.IntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "اسلاید گالری"
        verbose_name_plural = "گالری تصاویر و ویدیوها"
        ordering = ['order']

    def __str__(self):
        return self.caption_title


# 7. مدل لینک‌های شبکه‌های اجتماعی
class SocialLink(models.Model):
    platform = models.CharField(max_length=50, verbose_name="نام پلتفرم")
    url = models.URLField(verbose_name="لینک")
    icon_class = models.CharField(max_length=100, verbose_name="کلاس آیکون")
    is_footer = models.BooleanField(default=True, verbose_name="نمایش در فوتر")
    is_floating = models.BooleanField(default=True, verbose_name="نمایش در آیکون شناور")
    order = models.IntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "لینک شبکه اجتماعی"
        verbose_name_plural = "لینک‌های شبکه‌های اجتماعی"
        ordering = ['order']

    def __str__(self):
        return self.platform

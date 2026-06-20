from django.db import models
from django.conf import settings

# class News(models.Model):
#     title = models.CharField(max_length=200, verbose_name="عنوان خبر")
#     category = models.CharField(max_length=100, verbose_name="دسته‌بندی")
#     summary = models.CharField(max_length=300, blank=True, verbose_name="خلاصه")
#     image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="تصویر")
#     link = models.CharField(max_length=500, blank=True, verbose_name="لینک")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

#     class Meta:
#         verbose_name = "خبر"
#         verbose_name_plural = "اخبار"
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title



# class Event(models.Model):
#     title = models.CharField(max_length=200, verbose_name="عنوان رویداد")
#     image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="تصویر")
#     date_jalali = models.CharField(max_length=50, verbose_name="تاریخ شمسی")
#     time = models.CharField(max_length=20, verbose_name="ساعت")
#     short_description = models.TextField(verbose_name="توضیحات کوتاه")
#     is_upcoming = models.BooleanField(default=True, verbose_name="رویداد آینده")
#     capacity = models.PositiveIntegerField(default=0, verbose_name="ظرفیت")
#     registered_count = models.PositiveIntegerField(default=0, verbose_name="تعداد ثبت‌نام‌ها")  
#     is_full = models.BooleanField(default=False, verbose_name="تکمیل شده")
    
#     class Meta:
#         verbose_name = "رویداد"
#         verbose_name_plural = "رویدادها"
#         ordering = ['date_jalali']

#     def __str__(self):
#         return self.title



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



class Honor(models.Model):
    competition_name = models.CharField(max_length=200, verbose_name="عنوان جشنواره یا مسابقه")
    rank = models.CharField(max_length=200, verbose_name="مقام")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    image = models.ImageField(upload_to='honors/', blank=True, null=True, verbose_name="تصویر افتخار")
    is_featured = models.BooleanField(default=False, verbose_name="نمایش در صفحه اصلی")
    
    class Meta:
        verbose_name = "افتخار"
        verbose_name_plural = "افتخارات"
        ordering = ['order']

    def __str__(self):
        return f"{self.competition_name} - {self.rank}"



class AboutInfo(models.Model):
    description = models.TextField(verbose_name="توضیحات درباره ما")
    active_members = models.IntegerField(default=0, verbose_name="تعداد اعضای فعال")
    events_held = models.IntegerField(default=0, verbose_name="تعداد رویدادهای برگزار شده")
    total_resources = models.IntegerField(default=0, verbose_name="تعداد منابع علمی")
    button_text = models.CharField(
        max_length=200, 
        default="همین حالا به خانواده بزرگ انجمن علمی مکانیک بپیوندید", 
        verbose_name="متن دکمه"
    )
    button_link = models.CharField(
        max_length=200, 
        default="/login/", 
        verbose_name="لینک دکمه"
    )

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return "درباره انجمن علمی مکانیک"



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



class SocialLink(models.Model):
    platform = models.CharField(max_length=50, verbose_name="نام پلتفرم")
    url = models.URLField(verbose_name="لینک")
    icon_class = models.CharField(max_length=100, blank=True, verbose_name="کلاس آیکون") 
    is_footer = models.BooleanField(default=True, verbose_name="نمایش در فوتر")
    is_floating = models.BooleanField(default=True, verbose_name="نمایش در آیکون شناور")
    order = models.IntegerField(default=0, verbose_name="ترتیب")
    icon_image = models.ImageField(upload_to='social_icons/', blank=True, null=True, verbose_name="تصویر آیکون")

    class Meta:
        verbose_name = "لینک شبکه اجتماعی"
        verbose_name_plural = "لینک‌های شبکه‌های اجتماعی"
        ordering = ['order']

    def __str__(self):
        return self.platform

#_______________________________________
# REGISTRATION_STATUS_CHOICES = [
#     ('pending', 'در انتظار تایید'),
#     ('confirmed', 'تایید شده'),
#     ('cancelled', 'لغو شده'),
#     ('attended', 'حضور یافته'),
# ]

# class Registration(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE, 
#         verbose_name="کاربر",
#         related_name='registrations'
#     )
#     event = models.ForeignKey(
#         Event, 
#         on_delete=models.CASCADE, 
#         verbose_name="رویداد",
#         related_name='registrations'
#     )
#     registration_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
#     status = models.CharField(
#         max_length=20, 
#         choices=REGISTRATION_STATUS_CHOICES,
#         default='pending', 
#         verbose_name="وضعیت"
#     )
#     phone = models.CharField(max_length=15, blank=True, verbose_name="شماره تماس")
#     notes = models.TextField(blank=True, verbose_name="توضیحات")
    
#     class Meta: 
#         verbose_name = "ثبت‌نام"
#         verbose_name_plural = "ثبت‌نام‌ها"
#         unique_together = ['user', 'event']
#         ordering = ['-registration_date']

#     def __str__(self):
#         return f"{self.user.get_full_name()} - {self.event.title}"
#_______________________________________
class IndustryService(models.Model):
    """خدمات دانشکده به صنعت"""
    title = models.CharField(max_length=200, verbose_name="عنوان خدمت")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='industry/', blank=True, null=True, verbose_name="تصویر")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    # اطلاعات مسئول
    manager_name = models.CharField(max_length=200, blank=True, verbose_name="نام مسئول")
    manager_phone = models.CharField(max_length=20, blank=True, verbose_name="شماره تماس مسئول")
    manager_email = models.EmailField(blank=True, verbose_name="ایمیل مسئول")
    manager_room = models.CharField(max_length=50, blank=True, verbose_name="شماره اتاق")
    
    # اهداف (برای کوآپ)
    goals = models.TextField(blank=True, verbose_name="اهداف (هر هدف در یک خط)")

    class Meta:
        verbose_name = "خدمات صنعت"
        verbose_name_plural = "خدمات دانشکده به صنعت"
        ordering = ['order']

    def __str__(self):
        return self.title
    
    def get_goals_list(self):
        """برگرداندن اهداف به صورت لیست"""
        if self.goals:
            return [goal.strip() for goal in self.goals.split('\n') if goal.strip()]
        return []
#______________________call us_________________
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    #__________________
from django.shortcuts import render

from django.shortcuts import render
from .models import (
    News, Event, Resource, Honor, AboutInfo, GalleryItem, SocialLink
)


def home(request):
    context = {
        'news': News.objects.all()[:3],  # ۳ خبر آخر
        'events': Event.objects.filter(is_upcoming=True)[:3],  # ۳ رویداد آینده
        'resources': Resource.objects.all()[:3],  # ۳ منبع علمی
        'honors': Honor.objects.all(),  # همه افتخارات
        'about': AboutInfo.objects.first(),  # اطلاعات درباره ما
        'gallery_items': GalleryItem.objects.all(),  # همه اسلایدها
        'footer_socials': SocialLink.objects.filter(is_footer=True),  # لینک‌های فوتر
        'floating_socials': SocialLink.objects.filter(is_floating=True),  # لینک‌های شناور
    }
    return render(request, 'index-pages/index.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from .models import (
    News, Event, Resource, Honor, AboutInfo, GalleryItem, SocialLink
)
import os

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


def all_news(request):
    """نمایش همه اخبار با صفحه‌بندی"""
    news_list = News.objects.all()
    
    # صفحه‌بندی (۶ خبر در هر صفحه)
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # دریافت لیست دسته‌بندی‌ها برای فیلتر
    categories = News.objects.values_list('category', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'index-pages/news.html', context)


def news_detail(request, pk):
    """نمایش جزئیات یک خبر"""
    news = get_object_or_404(News, pk=pk)
    
    # اخبار مرتبط (همان دسته‌بندی، به جز خود خبر)
    related_news = News.objects.filter(category=news.category).exclude(pk=pk)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'index-pages/news_detail.html', context)



def all_events(request):
    """نمایش همه رویدادها"""
    # فیلتر بر اساس آینده یا گذشته
    show_upcoming = request.GET.get('show', 'upcoming') == 'upcoming'
    
    if show_upcoming:
        events = Event.objects.filter(is_upcoming=True)
    else:
        events = Event.objects.filter(is_upcoming=False)
    
    # صفحه‌بندی (۶ رویداد در هر صفحه)
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'show_upcoming': show_upcoming,
    }
    return render(request, 'index-pages/events.html', context)


def all_resources(request):
    """نمایش همه منابع علمی"""
    resources = Resource.objects.all()
    
    # صفحه‌بندی (۹ منبع در هر صفحه)
    paginator = Paginator(resources, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'index-pages/sources.html', context)



@login_required
def download_resource(request, pk):
    """دانلود فایل منبع علمی (فقط کاربران لاگین شده)"""
    resource = get_object_or_404(Resource, pk=pk)
    
    # بررسی وجود فایل
    if resource.file and resource.file.path:
        # افزایش شمارش دانلود
        resource.download_count += 1
        resource.save()
        
        # باز کردن و ارسال فایل
        file_path = resource.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
    
    raise Http404("فایل مورد نظر یافت نشد")



def about(request):
    """صفحه درباره ما"""
    about_info = AboutInfo.objects.first()
    context = {
        'about': about_info,
    }
    return render(request, 'index-pages/about.html', context)




def honors(request):
    """صفحه افتخارات"""
    honors_list = Honor.objects.all()
    context = {
        'honors': honors_list,
    }
    return render(request, 'index-pages/honors.html', context)


def contact(request):
    """صفحه تماس با ما"""
    footer_socials = SocialLink.objects.filter(is_footer=True)
    context = {
        'social_links': footer_socials,
    }
    return render(request, 'index-pages/call-us.html', context)



def industry(request):
    """صفحه ارتباط با صنعت"""
    return render(request, 'index-pages/industry.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Resource, Honor, AboutInfo, 
    GalleryItem, SocialLink, IndustryService  # <-- IndustryService رو اضافه کن
)
from .models import (
    Resource, Honor, AboutInfo, 
    GalleryItem, SocialLink
)
from events.models import Registration
from news.models import News
from events.models import Event
from members.models import GalleryImage, Committee, Member, MemberRequest
import os
from professor.models import EventProposal
from itertools import chain 
def home(request):
    """نمایش صفحه اصلی با تمام بخش‌ها"""
     # ✅ دریافت رویدادهای تایید شده از پیشنهادات اساتید
    approved_proposals = EventProposal.objects.filter(
        status='approved'
    ).select_related('professor').order_by('-created_at')[:3]
    
    # ✅ دریافت رویدادهای عادی (آینده)
    upcoming_events = Event.objects.filter(
        status='upcoming'
    ).order_by('-created_at')[:3]
    
    # ✅ ترکیب دو لیست (اختیاری)
    # از itertools.chain استفاده کن یا هر دو رو جداگانه بفرست
    
    context = {
        
        'news': News.objects.filter(is_published=True)[:3],
        'approved_proposals': approved_proposals,
        'events': upcoming_events,
        'resources': Resource.objects.all()[:3],
        'honors': Honor.objects.filter(is_featured=True)[:3],
        'about': AboutInfo.objects.first(),
        'gallery_items': GalleryImage.objects.all().order_by('-created_at'),  # ⭐ فقط جدید
        'footer_socials': SocialLink.objects.filter(is_footer=True),
        'floating_socials': SocialLink.objects.filter(is_floating=True),
    }
    return render(request, 'index-pages/index.html', context)

from itertools import chain
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from events.models import Event
from professor.models import EventProposal  # ✅ اضافه کن


def all_events(request):
    """نمایش همه رویدادها با فیلتر و جستجو"""
    show_upcoming = request.GET.get('show', 'upcoming') == 'upcoming'
    
    # ==========================================
    # دریافت رویدادهای عادی
    # ==========================================
    if show_upcoming:
        events = Event.objects.filter(status='upcoming')
    else:
        events = Event.objects.filter(status='completed')
    
    # ==========================================
    # دریافت پیشنهادات تایید شده از اساتید
    # ==========================================
    proposals = EventProposal.objects.filter(status='approved')
    
    # ==========================================
    # ترکیب دو لیست
    # ==========================================
    all_events = list(chain(events, proposals))
    
    # ==========================================
    # جستجو (بعد از ترکیب)
    # ==========================================
    search_query = request.GET.get('search')
    if search_query:
        # فیلتر کردن لیست ترکیبی
        filtered_events = []
        for item in all_events:
            title_match = search_query.lower() in item.title.lower()
            desc_match = hasattr(item, 'description') and search_query.lower() in item.description.lower()
            short_desc_match = hasattr(item, 'short_description') and search_query.lower() in item.short_description.lower()
            
            if title_match or desc_match or short_desc_match:
                filtered_events.append(item)
        all_events = filtered_events
    
    # ==========================================
    # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
    # ==========================================
    all_events.sort(key=lambda x: x.created_at, reverse=True)
    
    # ==========================================
    # صفحه‌بندی
    # ==========================================
    paginator = Paginator(all_events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'show_upcoming': show_upcoming,
        'search_query': search_query,
    }
    return render(request, 'index-pages/events.html', context)


def event_detail(request, pk):
    """نمایش جزئیات یک رویداد"""
    event = get_object_or_404(Event, pk=pk)
    
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user, 
            event=event
        ).exists()
    
    registered_count = Registration.objects.filter(event=event).count()
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'registered_count': registered_count,
    }
    return render(request, 'index-pages/details-pages/event.html', context)


@login_required
def register_event(request, pk):
    """ثبت‌نام کاربر در رویداد"""
    event = get_object_or_404(Event, pk=pk)
    
    # بررسی اینکه رویداد آینده است
    if event.status != 'upcoming':  # ✅ تغییر
        messages.error(request, 'این رویداد به پایان رسیده است.')
        return redirect('event_detail', pk=pk)
    
    # بررسی اینکه رویداد پر نشده باشد
    if event.is_full:
        messages.error(request, 'ظرفیت این رویداد تکمیل شده است.')
        return redirect('event_detail', pk=pk)
    
    # بررسی اینکه کاربر قبلاً ثبت‌نام کرده باشد
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'شما قبلاً در این رویداد ثبت‌نام کرده‌اید.')
        return redirect('event_detail', pk=pk)
    
    # بررسی ظرفیت
    if event.capacity > 0:
        current_registrations = Registration.objects.filter(event=event).count()
        if current_registrations >= event.capacity:
            event.is_full = True
            event.save()
            messages.error(request, 'ظرفیت این رویداد تکمیل شده است.')
            return redirect('event_detail', pk=pk)
    
    # ایجاد ثبت‌نام
    Registration.objects.create(
        user=request.user,
        event=event,
        status='pending'
    )
    
    # به‌روزرسانی تعداد ثبت‌نام‌ها
    event.registered_count = Registration.objects.filter(event=event).count()
    if event.capacity > 0 and event.registered_count >= event.capacity:
        event.is_full = True
    event.save()
    
    messages.success(request, f'ثبت‌نام شما در رویداد "{event.title}" با موفقیت انجام شد.')
    return redirect('event_detail', pk=pk)


@login_required
def cancel_registration(request, pk):
    """لغو ثبت‌نام کاربر در رویداد"""
    registration = get_object_or_404(Registration, user=request.user, event__id=pk)
    event = registration.event
    
    # فقط رویدادهای آینده قابل لغو هستند
    if event.status != 'upcoming':  # ✅ تغییر
        messages.error(request, 'این رویداد به پایان رسیده و قابل لغو نیست.')
        return redirect('event_detail', pk=pk)
    
    registration.delete()
    
    # به‌روزرسانی تعداد ثبت‌نام‌ها
    event.registered_count = Registration.objects.filter(event=event).count()
    if event.is_full and event.registered_count < event.capacity:
        event.is_full = False
    event.save()
    
    messages.success(request, f'ثبت‌نام شما در رویداد "{event.title}" با موفقیت لغو شد.')
    return redirect('event_detail', pk=pk)


def all_resources(request):
    """نمایش همه منابع علمی با جستجو"""
    resources = Resource.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(resources, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'index-pages/sources.html', context)


@login_required
def download_resource(request, pk):
    """دانلود فایل منبع علمی (فقط کاربران لاگین شده)"""
    resource = get_object_or_404(Resource, pk=pk)
    
    if resource.file and resource.file.path:
        resource.download_count += 1
        resource.save()
        
        file_path = resource.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
    
    raise Http404("فایل مورد نظر یافت نشد")


def honors(request):
    """صفحه افتخارات با صفحه‌بندی"""
    honors_list = Honor.objects.all()
    
    paginator = Paginator(honors_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'index-pages/honors.html', context)


def about(request):
    """صفحه درباره ما"""
    about_info = AboutInfo.objects.first()
    context = {
        'about': about_info,
    }
    return render(request, 'index-pages/about.html', context)


from .models import ContactMessage

def contact(request):
    """صفحه تماس با ما"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # ذخیره در دیتابیس
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'پیام شما با موفقیت ارسال شد.')
        return redirect('contact')
    
    return render(request, 'index-pages/call-us.html')

def industry(request):
    """صفحه ارتباط با صنعت"""
    services = IndustryService.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services,
    }
    return render(request, 'index-pages/industry.html', context)

def register(request):
    """صفحه ثبت‌نام کاربر"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """صفحه ورود کاربر"""
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'login.html')


def verify_view(request):
    """صفحه تایید (برای کاربران دانشجو)"""
    return render(request, 'verify.html')


def student_view(request):
    """صفحه دانشجویی (برای کاربران ویژه)"""
    return render(request, 'student.html')


@login_required
def user_dashboard(request):
    """پنل کاربری برای نمایش ثبت‌نام‌ها و فعالیت‌ها"""
    registrations = Registration.objects.filter(user=request.user).order_by('-registration_date')
    
    stats = {
        'total_registrations': registrations.count(),
        'pending_registrations': registrations.filter(status='pending').count(),
        'confirmed_registrations': registrations.filter(status='confirmed').count(),
        'attended_registrations': registrations.filter(status='attended').count(),
    }
    
    context = {
        'registrations': registrations,
        'stats': stats,
    }
    return render(request, 'index-pages/dashboard.html', context)





#------membership
from django.shortcuts import render

#------membership

@login_required
def membership_page(request):
    """صفحه عضویت در انجمن"""

    if Member.objects.filter(user=request.user).exists():
        messages.info(request, 'شما همین الان عضو انجمن هستید.')
        return redirect('home')

    if MemberRequest.objects.filter(user=request.user, status='pending').exists():
        messages.warning(request, 'درخواست عضویت شما در حال بررسی است.')
        return redirect('home')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        committee_id = request.POST.get('committee')
        message_text = request.POST.get('message', '')
        rules_agreed = request.POST.get('rules_agreed')

        if not rules_agreed:
            messages.error(request, 'برای ثبت درخواست باید قوانین را بپذیرید.')
            return redirect('membership_page')

        if not student_id or not committee_id:
            messages.error(request, 'لطفاً شماره دانشجویی و کمیته را وارد کنید.')
            return redirect('membership_page')

        committee = Committee.objects.filter(id=committee_id).first()
        if not committee:
            messages.error(request, 'کمیته انتخاب‌شده معتبر نیست.')
            return redirect('membership_page')

        if Member.objects.filter(student_id=student_id).exists() or \
           MemberRequest.objects.filter(student_id=student_id, status='pending').exists():
            messages.error(request, 'این شماره دانشجویی قبلاً ثبت شده است.')
            return redirect('membership_page')

        MemberRequest.objects.create(
            user=request.user,
            committee=committee,
            student_id=student_id,
            message=message_text,
            status='pending'
        )

        messages.success(request, 'درخواست عضویت شما با موفقیت ثبت شد.')
        return redirect('home')

    committees = Committee.objects.all()
    return render(request, 'membership.html', {'committees': committees})
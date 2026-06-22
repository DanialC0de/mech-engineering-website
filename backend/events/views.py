from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Event, Registration

def event_list(request):
    """نمایش همه رویدادها با فیلتر"""
    show_upcoming = request.GET.get('show', 'upcoming') == 'upcoming'
    
    if show_upcoming:
        events = Event.objects.filter(status='upcoming')
    else:
        events = Event.objects.filter(status='completed')
    
    search_query = request.GET.get('search')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query)
        )
    
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'show_upcoming': show_upcoming,
        'search_query': search_query,
    }
    return render(request, 'index-pages/events.html', context)  # <-- مسیر قبلی

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # ثبت‌نام کاربر
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user,
            event=event
        ).exists()

    # 🔥 تعداد ثبت‌نام معتبر (مهم)
    registered_count = event.registrations.filter(
        status__in=['pending', 'confirmed']
    ).count()

    # 🔥 ظرفیت باقی‌مانده (تمیز و safe)
    if event.capacity and event.capacity > 0:
        remaining_capacity = max(0, event.capacity - registered_count)
    else:
        remaining_capacity = None  # نامحدود

    # سرفصل‌ها
    syllabus_list = []
    if event.syllabus:
        syllabus_list = [
            item.strip()
            for item in event.syllabus.split('\n')
            if item.strip()
        ]

        return render(request, 'index-pages/details-pages/event.html', {
        'event': event,
        'is_registered': is_registered,
        'registered_count': registered_count,
        'remaining_capacity': remaining_capacity,
        'syllabus_list': syllabus_list,
    })
@login_required
def register_event(request, pk):
    """ثبت‌نام کاربر در رویداد"""
    event = get_object_or_404(Event, pk=pk)
    
    # بررسی امکان ثبت‌نام
    if not event.can_register:
        if event.status == 'completed':
            messages.error(request, 'این رویداد به پایان رسیده است.')
        elif event.is_full:
            messages.error(request, 'ظرفیت این رویداد تکمیل شده است.')
        else:
            messages.error(request, 'ثبت‌نام در این رویداد امکان‌پذیر نیست.')
        return redirect('events:detail', pk=pk)
    
    # بررسی ثبت‌نام تکراری
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'شما قبلاً در این رویداد ثبت‌نام کرده‌اید.')
        return redirect('events:detail', pk=pk)
    
    # ایجاد ثبت‌نام
    Registration.objects.create(
        user=request.user,
        event=event,
        status='confirmed'
    )
    
    # به‌روزرسانی تعداد ثبت‌نام‌ها
    event.update_registration_count()
    
    messages.success(request, f'ثبت‌نام شما در رویداد "{event.title}" با موفقیت انجام شد.')
    return redirect('events:detail', pk=pk)

@login_required
def cancel_registration(request, pk):
    """لغو ثبت‌نام کاربر در رویداد"""
    registration = get_object_or_404(Registration, user=request.user, event__id=pk)
    event = registration.event
    
    # فقط رویدادهای آینده قابل لغو هستند
    if event.status == 'completed':
        messages.error(request, 'این رویداد به پایان رسیده و قابل لغو نیست.')
        return redirect('events:detail', pk=pk)
    
    registration.delete()
    
    # به‌روزرسانی تعداد ثبت‌نام‌ها
    event.update_registration_count()
    
    messages.success(request, f'ثبت‌نام شما در رویداد "{event.title}" با موفقیت لغو شد.')
    return redirect('events:detail', pk=pk)
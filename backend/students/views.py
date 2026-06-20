# students/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
import json

from accounts.models import CustomUser
from events.models import Event, Registration
from news.models import News
from .models import StudentProfile  # ✅ اینجا درست است


@login_required
def student_panel(request):
    """نمایش پنل دانشجو"""
    if request.user.role != 'student':
        messages.error(request, 'شما دسترسی به این بخش ندارید')
        return redirect('home')
    
    # گرفتن پروفایل دانشجو
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student = None
    
    return render(request, 'student.html', {
        'user': request.user,
        'student': student,  # ✅ اضافه شد
    })


@login_required
def get_dashboard_data(request):
    """دریافت اطلاعات داشبورد به صورت JSON"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    # تعداد ثبت‌نام‌های تأیید شده
    my_registrations = Registration.objects.filter(
        user=request.user,
        status='confirmed'
    ).count()
    
    # تعداد منابع جدید
    from events.models import Resource
    new_resources = Resource.objects.count()
    
    # تعداد تیکت‌ها (اگر مدل تیکت دارید)
    my_tickets = 0
    
    # آخرین اطلاعیه‌ها
    announcements = News.objects.filter(
        is_published=True,
        category='announcement'
    ).order_by('-created_at')[:5]
    
    # رویدادهای قابل ثبت‌نام
    available_events = Event.objects.filter(
        status='upcoming',
        is_full=False
    ).exclude(
        registrations__user=request.user
    )[:5]
    
    # رویدادهای ثبت‌نام شده من
    my_events = Registration.objects.filter(
        user=request.user,
        status__in=['pending', 'confirmed']
    ).select_related('event')[:10]
    
    data = {
        'stats': {
            'myRegistrations': my_registrations,
            'newResources': new_resources,
            'myTickets': my_tickets,
        },
        'announcements': [
            {
                'id': news.id,
                'title': news.title,
                'created_at': news.jalali_date,
                'summary': news.summary[:100] + '...' if len(news.summary) > 100 else news.summary
            }
            for news in announcements
        ],
        'availableEvents': [
            {
                'id': event.id,
                'title': event.title,
                'date': event.jalali_date,
                'time': event.time,
                'remaining': event.capacity - event.registered_count if event.capacity > 0 else 'نامحدود',
                'capacity': event.capacity,
                'registered_count': event.registered_count
            }
            for event in available_events
        ],
        'myEvents': [
            {
                'id': reg.id,
                'event_id': reg.event.id,
                'title': reg.event.title,
                'date': reg.event.jalali_date,
                'status': dict(Registration.STATUS_CHOICES).get(reg.status, 'نامشخص'),
                'status_class': {
                    'pending': 'warning',
                    'confirmed': 'success',
                    'cancelled': 'danger'
                }.get(reg.status, 'secondary')
            }
            for reg in my_events
        ]
    }
    
    return JsonResponse(data)


@login_required
def get_events_list(request):
    """دریافت لیست همه رویدادها با فیلتر"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    status_filter = request.GET.get('status', 'all')
    
    events = Event.objects.all()
    
    if status_filter != 'all':
        events = events.filter(status=status_filter)
    
    data = []
    for event in events:
        is_registered = Registration.objects.filter(
            event=event,
            user=request.user,
            status__in=['pending', 'confirmed']
        ).exists()
        
        registration_id = None
        if is_registered:
            reg = Registration.objects.filter(
                event=event,
                user=request.user,
                status__in=['pending', 'confirmed']
            ).first()
            if reg:
                registration_id = reg.id
        
        data.append({
            'id': event.id,
            'title': event.title,
            'date': event.jalali_date,
            'time': event.time,
            'status': dict(Event.STATUS_CHOICES).get(event.status, ''),
            'status_class': {
                'upcoming': 'primary',
                'ongoing': 'warning',
                'completed': 'secondary'
            }.get(event.status, 'secondary'),
            'is_registered': is_registered,
            'registration_id': registration_id,
            'is_full': event.is_full,
            'capacity': event.capacity,
            'registered_count': event.registered_count,
            'remaining': event.capacity - event.registered_count if event.capacity > 0 else 'نامحدود'
        })
    
    return JsonResponse({'events': data})


@login_required
@require_http_methods(["POST"])
def register_event(request, event_id):
    """ثبت‌نام دانشجو در رویداد"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    event = get_object_or_404(Event, id=event_id)
    
    # بررسی امکان ثبت‌نام
    if not event.can_register():
        return JsonResponse({
            'success': False,
            'error': 'امکان ثبت‌نام در این رویداد وجود ندارد'
        }, status=400)
    
    # بررسی ثبت‌نام قبلی
    if Registration.objects.filter(event=event, user=request.user).exists():
        return JsonResponse({
            'success': False,
            'error': 'شما قبلاً در این رویداد ثبت‌نام کرده‌اید'
        }, status=400)
    
    # ایجاد ثبت‌نام
    registration = Registration.objects.create(
        event=event,
        user=request.user,
        status='confirmed'
    )
    
    # به‌روزرسانی تعداد ثبت‌نام‌ها
    event.update_registration_count()
    
    return JsonResponse({
        'success': True,
        'message': f'ثبت‌نام شما در رویداد "{event.title}" با موفقیت انجام شد',
        'registration_id': registration.id
    })


@login_required
@require_http_methods(["POST"])
def cancel_registration(request, registration_id):
    """لغو ثبت‌نام دانشجو"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    registration = get_object_or_404(
        Registration,
        id=registration_id,
        user=request.user
    )
    
    if registration.status == 'cancelled':
        return JsonResponse({
            'success': False,
            'error': 'این ثبت‌نام قبلاً لغو شده است'
        }, status=400)
    
    # لغو ثبت‌نام
    registration.status = 'cancelled'
    registration.save()
    
    # به‌روزرسانی تعداد ثبت‌نام‌های رویداد
    registration.event.update_registration_count()
    
    return JsonResponse({
        'success': True,
        'message': f'ثبت‌نام شما در رویداد "{registration.event.title}" لغو شد'
    })

@login_required
def get_resources_list(request):
    """دریافت لیست منابع علمی با فیلتر"""
    try:
        if request.user.role != 'student':
            return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
        
        from website.models import Resource  # ✅ ایمپورت داخل تابع
        
        print("=== شروع get_resources_list ===")
        
        resources = Resource.objects.all().order_by('-id')
        print(f"تعداد منابع: {resources.count()}")
        
        data = []
        for resource in resources:
            data.append({
                'id': resource.id,
                'title': resource.title,
                'description': resource.description[:150] + '...' if len(resource.description) > 150 else resource.description,
                'download_count': resource.download_count,
                'has_file': bool(resource.file),
                'file_url': resource.file.url if resource.file else None,
                'image_url': resource.image.url if resource.image else None
            })
        
        print(f"تعداد داده: {len(data)}")
        print("=== پایان get_resources_list ===")
        
        return JsonResponse({'resources': data})
        
    except Exception as e:
        print(f"❌ خطا در get_resources_list: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

@login_required
def download_resource(request, resource_id):
    """دانلود فایل منبع علمی"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    from website.models import Resource  # ✅ ایمپورت داخل تابع
    
    resource = get_object_or_404(Resource, id=resource_id)
    
    if not resource.file:
        return JsonResponse({
            'success': False,
            'error': 'فایلی برای این منبع وجود ندارد'
        }, status=404)
    
    resource.download_count += 1
    resource.save()
    
    return redirect(resource.file.url)

@login_required
def get_profile_data(request):
    """دریافت اطلاعات پروفایل کاربر"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    user = request.user
    
    # تعداد رویدادهای شرکت کرده
    event_count = Registration.objects.filter(
        user=user,
        status='confirmed'
    ).count()
    
    # تعداد دانلودها
    download_count = 0
    
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
        'role': dict(CustomUser.ROLE_CHOICES).get(user.role, ''),
        'event_count': event_count,
        'download_count': download_count,
        'joined_date': user.date_joined.strftime('%Y/%m/%d') if user.date_joined else ''
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def change_password(request):
    """تغییر رمز عبور کاربر"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    data = json.loads(request.body)
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    if not new_password or not confirm_password:
        return JsonResponse({'error': 'رمز عبور را وارد کنید'}, status=400)
    
    if new_password != confirm_password:
        return JsonResponse({'error': 'رمز عبور با تکرار آن مطابقت ندارد'}, status=400)
    
    if len(new_password) < 8:
        return JsonResponse({'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد'}, status=400)
    
    # تغییر رمز عبور
    request.user.set_password(new_password)
    request.user.save()
    
    # نگه داشتن نشست کاربر
    update_session_auth_hash(request, request.user)
    
    return JsonResponse({'success': True, 'message': 'رمز عبور با موفقیت تغییر کرد'})
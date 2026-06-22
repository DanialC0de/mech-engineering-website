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
from .models import ProfessorProfile, EventInvitation


# ==================== دکوریتور سفارشی ====================
def professor_or_superuser_required(view_func):
    """دکوریتور برای اجازه دسترسی به اساتید و سوپر یوزرها"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'لطفاً ابتدا وارد شوید')
            return redirect('accounts:login')
        
        # اجازه دسترسی به professors و superusers
        if request.user.role == 'professor' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # برای درخواست‌های AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
        
        messages.error(request, 'شما دسترسی به این بخش ندارید')
        return redirect('home')
    return wrapper


# ==================== ویوهای پنل استاد ====================

@login_required
@professor_or_superuser_required
def professor_panel(request):
    """نمایش پنل استاد"""
    # گرفتن پروفایل استاد
    try:
        professor = request.user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = None
    
    return render(request, 'professor.html', {
        'user': request.user,
        'professor': professor,
    })


@login_required
@professor_or_superuser_required
def get_dashboard_data(request):
    """دریافت اطلاعات داشبورد به صورت JSON"""
    # رویدادهای پیش رو که استاد مدرس آن است
    upcoming_events = Event.objects.filter(
        instructor_name__icontains=request.user.get_full_name(),
        status='upcoming'
    ).count()
    
    # دعوتنامه‌های در انتظار
    pending_invitations = EventInvitation.objects.filter(
        professor=request.user,
        status='pending'
    ).count()
    
    # پیام‌های جدید (اگر سیستم پیام دارید)
    new_messages = 0
    
    # مقالات (این باید از مدل مقالات بیاید اگر دارید)
    my_articles = 0
    
    # لیست دعوتنامه‌ها
    invitations = EventInvitation.objects.filter(
        professor=request.user,
        status='pending'
    ).select_related('event')[:10]
    
    # رویدادهای من (پذیرفته شده)
    my_events = EventInvitation.objects.filter(
        professor=request.user,
        status='accepted'
    ).select_related('event')[:10]
    
    data = {
        'stats': {
            'upcomingEvents': upcoming_events,
            'invitations': pending_invitations,
            'newMessages': new_messages,
            'myArticles': my_articles,
        },
        'invitations': [
            {
                'id': inv.id,
                'event_id': inv.event.id,
                'title': inv.event.title,
                'date': inv.event.jalali_date,
                'role': dict(EventInvitation.ROLE_CHOICES).get(inv.role, 'نامشخص'),
                'status': dict(EventInvitation.STATUS_CHOICES).get(inv.status, 'نامشخص'),
                'message': inv.message or ''
            }
            for inv in invitations
        ],
        'myEvents': [
            {
                'id': inv.event.id,
                'title': inv.event.title,
                'date': inv.event.jalali_date,
                'time': inv.event.time,
                'role': dict(EventInvitation.ROLE_CHOICES).get(inv.role, 'نامشخص'),
                'registered_count': inv.event.registered_count
            }
            for inv in my_events
        ]
    }
    
    return JsonResponse(data)


@login_required
@professor_or_superuser_required
def get_events_list(request):
    """دریافت لیست همه رویدادها"""
    status_filter = request.GET.get('status', 'all')
    
    events = Event.objects.all()
    
    if status_filter != 'all':
        events = events.filter(status=status_filter)
    
    data = []
    for event in events:
        # بررسی آیا استاد در این رویداد دعوت شده
        has_invitation = EventInvitation.objects.filter(
            event=event,
            professor=request.user
        ).exists()
        
        invitation_status = None
        if has_invitation:
            inv = EventInvitation.objects.filter(
                event=event,
                professor=request.user
            ).first()
            if inv:
                invitation_status = inv.status
        
        data.append({
            'id': event.id,
            'title': event.title,
            'date': event.jalali_date,
            'time': event.time,
            'status': dict(Event.STATUS_CHOICES).get(event.status, 'نامشخص'),
            'capacity': event.capacity,
            'registered_count': event.registered_count,
            'instructor_name': event.instructor_name or '',
            'has_invitation': has_invitation,
            'invitation_status': invitation_status
        })
    
    return JsonResponse({'events': data})


@login_required
@professor_or_superuser_required
@require_http_methods(["POST"])
def respond_to_invitation(request, invitation_id):
    """پاسخ به دعوتنامه رویداد"""
    invitation = get_object_or_404(EventInvitation, id=invitation_id, professor=request.user)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'داده‌های ارسالی نامعتبر است'}, status=400)
    
    action = data.get('action')  # 'accept' or 'decline'
    
    if action == 'accept':
        invitation.status = 'accepted'
        message = 'دعوتنامه پذیرفته شد'
    elif action == 'decline':
        invitation.status = 'declined'
        message = 'دعوتنامه رد شد'
    else:
        return JsonResponse({'error': 'عملیات نامعتبر'}, status=400)
    
    invitation.save()
    
    return JsonResponse({'success': True, 'message': message})


@login_required
@professor_or_superuser_required
def get_profile_data(request):
    """دریافت اطلاعات پروفایل استاد"""
    user = request.user
    
    try:
        professor = user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = ProfessorProfile.objects.create(user=user)
    
    # آمار
    event_count = Event.objects.filter(instructor_name__icontains=user.get_full_name()).count()
    publication_count = 0  # این باید از مدل مقالات بیاید
    
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
        'employee_id': professor.employee_id if professor else '',
        'department': professor.department if professor else '',
        'academic_rank': professor.academic_rank if professor else '',
        'field_of_study': professor.field_of_study if professor else '',
        'office_number': professor.office_number if professor else '',
        'research_interests': professor.research_interests if professor else '',
        'publications': professor.publications if professor else '',
        'bio': professor.bio if professor else '',
        'avatar_url': professor.avatar.url if professor and professor.avatar else '',
        'role': dict(CustomUser.ROLE_CHOICES).get(user.role, ''),
        'event_count': event_count,
        'publication_count': publication_count,
    }
    
    return JsonResponse(data)


@login_required
@professor_or_superuser_required
@require_http_methods(["POST"])
def update_profile_data(request):
    """به‌روزرسانی اطلاعات پروفایل استاد"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'داده‌های ارسالی نامعتبر است'}, status=400)
    
    user = request.user
    
    try:
        professor = user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = ProfessorProfile.objects.create(user=user)
    
    # به‌روزرسانی اطلاعات کاربر
    first_name = str(data.get('first_name', '')).strip()
    last_name = str(data.get('last_name', '')).strip()
    email = str(data.get('email', '')).strip()
    phone_number = str(data.get('phone_number', '')).strip()
    
    if not first_name or not last_name:
        return JsonResponse({'success': False, 'error': 'نام و نام خانوادگی الزامی است'}, status=400)
    
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone_number = phone_number
    user.save(update_fields=['first_name', 'last_name', 'email', 'phone_number'])
    
    # به‌روزرسانی اطلاعات پروفایل استاد
    professor.employee_id = str(data.get('employee_id', '')).strip() or None
    professor.department = str(data.get('department', '')).strip()
    professor.academic_rank = str(data.get('academic_rank', '')).strip()
    professor.field_of_study = str(data.get('field_of_study', '')).strip()
    professor.office_number = str(data.get('office_number', '')).strip()
    professor.research_interests = str(data.get('research_interests', '')).strip()
    professor.publications = str(data.get('publications', '')).strip()
    professor.bio = str(data.get('bio', '')).strip()
    professor.save()
    
    return JsonResponse({'success': True, 'message': 'اطلاعات پروفایل با موفقیت ذخیره شد'})


@login_required
@professor_or_superuser_required
@require_http_methods(["POST"])
def change_password(request):
    """تغییر رمز عبور کاربر"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'داده‌های ارسالی نامعتبر است'}, status=400)
    
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
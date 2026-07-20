from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import json
from website.models import Resource

from accounts.decorators import role_required
from accounts.models import CustomUser
from events.models import Event
from .models import ProfessorProfile, EventInvitation, ProfessorArticle, EventProposal


@login_required
@role_required(['professor'])
def professor_panel(request):
    try:
        professor = request.user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = None
    return render(request, 'professor.html', {
        'user': request.user,
        'professor': professor,
    })


@login_required
@role_required(['professor'])
def get_dashboard_data(request):
    upcoming_events = Event.objects.filter(
        instructor_name__icontains=request.user.get_full_name(),
        status='upcoming'
    ).count()
    
    my_articles = ProfessorArticle.objects.filter(professor=request.user).count()
    
    data = {
        'stats': {
            'upcomingEvents': upcoming_events,
            'myArticles': my_articles,
        }
    }
    return JsonResponse(data)


@login_required
@role_required(['professor'])
def get_invitations_list(request):
    invitations = EventInvitation.objects.filter(
        professor=request.user
    ).select_related('event').order_by('-created_at')
    
    data = []
    for inv in invitations:
        data.append({
            'id': inv.id,
            'event_id': inv.event.id,
            'title': inv.event.title,
            'date': inv.event.jalali_date,
            'time': inv.event.time,
            'role': dict(EventInvitation.ROLE_CHOICES).get(inv.role, 'نامشخص'),
            'status': inv.status,
            'status_display': dict(EventInvitation.STATUS_CHOICES).get(inv.status, 'نامشخص'),
            'status_class': {
                'pending': 'warning',
                'accepted': 'success',
                'declined': 'danger'
            }.get(inv.status, 'secondary'),
            'message': inv.message or '',
            'created_at': inv.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return JsonResponse({'invitations': data})


@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def respond_to_invitation(request, invitation_id):
    invitation = get_object_or_404(EventInvitation, id=invitation_id, professor=request.user)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'داده‌های ارسالی نامعتبر است'}, status=400)
    
    action = data.get('action')
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
@role_required(['professor'])
def get_events_list(request):

    events = Event.objects.all().order_by('-created_at')

    events_data = []

    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'date': event.jalali_date,
            'time': event.time,

            'status': event.get_status_display(),
            'detail_url': f'/events/{event.id}/',

            'status_class': {
                'upcoming': 'primary',
                'ongoing': 'warning',
                'completed': 'secondary'
            }.get(event.status, 'secondary'),

            'capacity': event.capacity,
            'registered_count': event.registered_count,

            'description': event.short_description,
            'full_description': event.full_description,

            'instructor_name': event.instructor_name,
            'instructor_title': event.instructor_title,

            'is_full': event.is_full,

            # برای رفتن به صفحه جزئیات
            'detail_url': f'/events/{event.id}/',
        })

    return JsonResponse({
        'events': events_data
    })
@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def propose_event(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'داده‌های ارسالی نامعتبر است'}, status=400)

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    proposed_date = data.get('date', '').strip()
    event_type = data.get('type', '').strip()

    if not all([title, description, proposed_date, event_type]):
        return JsonResponse({'success': False, 'error': 'تمامی فیلدها الزامی هستند'}, status=400)

    proposal = EventProposal.objects.create(
        professor=request.user,
        title=title,
        description=description,
        proposed_date=proposed_date,
        event_type=event_type,
        status='pending'
    )

    return JsonResponse({
        'success': True,
        'message': 'پیشنهاد شما با موفقیت ثبت شد و در انتظار تایید دبیر انجمن است.',
        'id': proposal.id
    })


@login_required
@role_required(['professor'])
def get_articles_list(request):
    articles = ProfessorArticle.objects.filter(professor=request.user).order_by('-created_at')
    data = {
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'author': request.user.get_full_name() or request.user.username,
                'date': article.created_at.strftime('%Y-%m-%d %H:%M'),
                'status': article.get_status_display(),
                'status_class': {
                    'draft': 'secondary',
                    'submitted': 'warning',
                    'approved': 'success',
                    'rejected': 'danger'
                }.get(article.status, 'secondary'),
                'file_url': article.file.url if article.file else None,
            }
            for article in articles
        ]
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def create_article(request):
    title = request.POST.get('title', '').strip()
    abstract = request.POST.get('abstract', '').strip()
    uploaded_file = request.FILES.get('file')

    if not title:
        return JsonResponse({'success': False, 'error': 'عنوان مقاله الزامی است'}, status=400)
    if not uploaded_file:
        return JsonResponse({'success': False, 'error': 'فایل مقاله الزامی است'}, status=400)
    if not uploaded_file.name.endswith('.pdf'):
        return JsonResponse({'success': False, 'error': 'فقط فایل‌های PDF مجاز هستند'}, status=400)

    article = ProfessorArticle.objects.create(
        professor=request.user,
        title=title,
        abstract=abstract,
        file=uploaded_file,
        status='submitted'
    )

    return JsonResponse({
        'success': True,
        'message': 'مقاله با موفقیت ارسال شد و در انتظار تایید دبیر انجمن است.',
        'id': article.id
    })


@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def delete_article(request, article_id):
    article = get_object_or_404(ProfessorArticle, id=article_id, professor=request.user)
    if article.status not in ['draft', 'submitted']:
        return JsonResponse({'success': False, 'error': 'این مقاله قابل حذف نیست'}, status=400)
    
    article.delete()
    return JsonResponse({'success': True, 'message': 'مقاله با موفقیت حذف شد'})


@login_required
@role_required(['professor'])
def get_profile_data(request):
    user = request.user
    try:
        professor = user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = ProfessorProfile.objects.create(user=user)
    
    event_count = Event.objects.filter(instructor_name__icontains=user.get_full_name()).count()
    publication_count = ProfessorArticle.objects.filter(professor=user).count()
    
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
        'position': professor.academic_rank or '',
        'faculty': professor.department or '',
        'expertise': professor.field_of_study or '',
        'bio': professor.bio or '',
        'avatar_url': professor.avatar.url if professor and professor.avatar else '',
        'article_count': publication_count,
    }
    return JsonResponse(data)


@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def update_profile_data(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'داده‌های ارسالی نامعتبر است'}, status=400)
    
    user = request.user
    try:
        professor = user.professor_profile
    except ProfessorProfile.DoesNotExist:
        professor = ProfessorProfile.objects.create(user=user)
    
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
    
    professor.academic_rank = str(data.get('position', '')).strip()
    professor.department = str(data.get('faculty', '')).strip()
    professor.field_of_study = str(data.get('expertise', '')).strip()
    professor.bio = str(data.get('bio', '')).strip()
    professor.save()
    
    return JsonResponse({'success': True, 'message': 'اطلاعات پروفایل با موفقیت ذخیره شد'})


@login_required
@role_required(['professor'])
@require_http_methods(["POST"])
def change_password(request):
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
    
    request.user.set_password(new_password)
    request.user.save()
    update_session_auth_hash(request, request.user)
    
    return JsonResponse({'success': True, 'message': 'رمز عبور با موفقیت تغییر کرد'})

@login_required
@role_required(['professor'])
def get_resources_list(request):

    resources = Resource.objects.all().order_by('-created_at')

    resources_data = []

    for resource in resources:
        resources_data.append({
            'id': resource.id,
            'title': resource.title,
            'category': resource.category,
            'description': resource.description,
            'download_count': resource.download_count,

            'file_url': (
                resource.file.url
                if resource.file
                else None
            ),

            'image_url': (
                resource.image.url
                if resource.image
                else None
            )
        })

    return JsonResponse({
        'resources': resources_data
    })

@login_required
@require_http_methods(["POST"])
def send_event_invitation(request):

    if not request.user.is_superuser:
        return JsonResponse({
            'success': False,
            'error': 'شما دسترسی ندارید'
        }, status=403)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({
            'success': False,
            'error': 'داده نامعتبر'
        }, status=400)

    professor_id = data.get('professor_id')
    event_id = data.get('event_id')

    role = data.get(
        'role',
        'instructor'
    )

    message = data.get(
        'message',
        ''
    )

    professor = get_object_or_404(
        CustomUser,
        id=professor_id
    )

    event = get_object_or_404(
        Event,
        id=event_id
    )

    invitation, created = EventInvitation.objects.get_or_create(
        professor=professor,
        event=event,
        defaults={
            'role': role,
            'message': message,
            'status': 'pending'
        }
    )

    if not created:
        return JsonResponse({
            'success': False,
            'error': 'قبلاً دعوتنامه ارسال شده است'
        })

    return JsonResponse({
        'success': True,
        'message': 'دعوتنامه با موفقیت ارسال شد'
    })

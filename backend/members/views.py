from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member, MemberRequest, Committee, InternalResource
from events.models import Event, Registration
from website.models import GalleryItem
from .models import GalleryImage
from professor.models import (
    ProfessorArticle,
    EventProposal,
    EventInvitation,
)
from django.utils import timezone
from django.contrib.auth import get_user_model 
User = get_user_model()
from professor.models import ProfessorProfile


# ✅ لیست نقش‌های مجاز برای مدیریت
ALLOWED_ROLES = ['head', 'vice', 'secretary', 'committee_head', 'member']


def check_member_access(request):
    """بررسی دسترسی کاربر (همه نقش‌ها مجاز هستن)"""
    try:
        member = Member.objects.get(user=request.user)
        return member
    except Member.DoesNotExist:
        messages.error(request, "شما عضو انجمن نیستید.")
        return None


@login_required
def member_dashboard(request):
    """پنل عضو انجمن"""
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.warning(request, 'شما عضو انجمن نیستید. درخواست عضویت ثبت کنید.')
        return render(request, 'member.html', {
            'member': None,
            'pending_requests': 0,
            'member_requests': [],
            'members': [],
            'committees': [],
            'internal_resources': [],
            'my_events': [],
            'all_my_events': [],
            'gallery_items': [],
            'suggested_articles': [],
            'suggested_events': [],
            'professors': [],
            'professor_invitations': [],
            'pending_articles': [],
            'approved_articles': [],
            'rejected_articles': [],
            'pending_proposals': [],
            'approved_proposals': [],
            'rejected_proposals': [],
        })
    
    # ==========================================
    # رویدادهای تحت مسئولیت کاربر
    # ==========================================
    my_events = Event.objects.filter(
        created_by=request.user
    ).order_by('-created_at')[:3]
    
    all_my_events = Event.objects.filter(
        created_by=request.user
    ).order_by('-created_at')
    
    # ==========================================
    # درخواست‌های عضویت (همه نقش‌ها میتونن ببینن)
    # ==========================================
    pending_requests = MemberRequest.objects.filter(status='pending')
    
    # ==========================================
    # اعضای انجمن
    # ==========================================
    members_list = Member.objects.filter(is_active=True).select_related('user', 'committee')
    
    # ==========================================
    # کمیته‌ها
    # ==========================================
    committees = Committee.objects.all()
    
    # ==========================================
    # منابع داخلی کاربر
    # ==========================================
    internal_resources = InternalResource.objects.filter(
        uploaded_by=request.user
    ).order_by('-created_at')
    
    # ==========================================
    # گالری تصاویر (از اپ members)
    # ==========================================
    gallery_items = GalleryImage.objects.all().order_by('-created_at')
    
    # ==========================================
    # ✅ مقالات پیشنهادی اساتید (همه مقالات)
    # ==========================================
    all_articles = ProfessorArticle.objects.all().select_related(
        'professor'
    ).order_by('-created_at')
    
    # تفکیک بر اساس وضعیت
    pending_articles = all_articles.filter(status='submitted')
    approved_articles = all_articles.filter(status='approved')
    rejected_articles = all_articles.filter(status='rejected')
    
    # مقالات برای نمایش در داشبورد (۱۰ مورد آخر)
    suggested_articles = all_articles[:10]
    
    # ==========================================
    # ✅ رویدادهای پیشنهادی اساتید (همه پیشنهادات)
    # ==========================================
    all_proposals = EventProposal.objects.all().select_related(
        'professor'
    ).order_by('-created_at')
    
    # تفکیک بر اساس وضعیت
    pending_proposals = all_proposals.filter(status='pending')
    approved_proposals = all_proposals.filter(status='approved')
    rejected_proposals = all_proposals.filter(status='rejected')
    
    # رویدادهای پیشنهادی برای نمایش در داشبورد (۲۰ مورد آخر)
    suggested_events = all_proposals[:20]
    
    # ==========================================
    # لیست اساتید برای دعوت (فقط کاربرانی که پروفایل استاد دارند)
    # ==========================================
    professors = User.objects.filter(
        professor_profile__isnull=False
    ).order_by('first_name', 'last_name')
    
    # ==========================================
    # دعوت‌نامه‌های ارسال شده توسط کاربر
    # ==========================================
    professor_invitations = EventInvitation.objects.filter(
        created_by=request.user
    ).select_related('event', 'professor').order_by('-created_at')
    
    # ==========================================
    # ساخت context
    # ==========================================
    context = {
        'member': member,
        'pending_requests': pending_requests.count(),
        'member_requests': pending_requests,
        'members': members_list,
        'committees': committees,
        'internal_resources': internal_resources,
        'my_events': my_events,
        'all_my_events': all_my_events,
        'gallery_items': gallery_items,
        'suggested_articles': suggested_articles,
        'suggested_events': suggested_events,
        'professors': professors,
        'professor_invitations': professor_invitations,
        'pending_articles': pending_articles,
        'approved_articles': approved_articles,
        'rejected_articles': rejected_articles,
        'pending_proposals': pending_proposals,
        'approved_proposals': approved_proposals,
        'rejected_proposals': rejected_proposals,
        'all_articles': all_articles,
        'all_proposals': all_proposals,
    }
    
    return render(request, 'member.html', context)


@login_required
def reject_request(request, pk):
    """رد درخواست عضویت"""
    if request.method != 'POST':
        messages.error(request, 'درخواست نامعتبر است.')
        return redirect('members:dashboard')

    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')

    member_request = get_object_or_404(
        MemberRequest,
        pk=pk,
        status='pending'
    )

    member_request.status = 'rejected'
    member_request.save(update_fields=['status'])

    messages.success(request, 'درخواست عضویت با موفقیت رد شد.')
    return redirect('members:dashboard')


@login_required
def approve_request(request, pk):
    """تأیید درخواست عضویت"""
    if request.method != 'POST':
        messages.error(request, 'درخواست نامعتبر است.')
        return redirect('members:dashboard')

    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')

    member_request = get_object_or_404(MemberRequest, pk=pk, status='pending')

    if Member.objects.filter(user=member_request.user).exists():
        # کاربر از قبل Member داره (مثلاً به خاطر یک تلاش ناقص قبلی)
        # پس فقط وضعیت درخواست و نقش کاربر رو هماهنگ می‌کنیم، رد نمی‌کنیم
        member_request.status = 'approved'
        member_request.save(update_fields=['status'])
        member_request.user.role = 'member'
        member_request.user.save(update_fields=['role'])
        messages.success(request, 'عضویت این کاربر تکمیل و تأیید شد.')
        return redirect('members:dashboard')

    if Member.objects.filter(student_id=member_request.student_id).exists():
        messages.error(request, f'شماره دانشجویی "{member_request.student_id}" قبلاً ثبت شده است.')
        member_request.status = 'rejected'
        member_request.save(update_fields=['status'])
        return redirect('members:dashboard')

    # ✅ فقط status رو عوض کن — ساخت Member رو خود متد save() مدل انجام می‌ده
    member_request.status = 'approved'
    member_request.save(update_fields=['status'])

    # ✅ هماهنگ‌سازی نقش کاربر
    member_request.user.role = 'member'
    member_request.user.save(update_fields=['role'])

    messages.success(request, 'درخواست عضویت با موفقیت تأیید شد.')
    return redirect('members:dashboard')

@login_required
def create_event(request):
    """ایجاد رویداد جدید"""
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        jalali_date = request.POST.get('date')
        time = request.POST.get('time')
        short_description = request.POST.get('short_description')
        try:
            capacity = int(request.POST.get("capacity", 0))
        except ValueError:
            capacity = 0
        image = request.FILES.get('image')
        
        if not title or not jalali_date or not time:
            messages.error(request, 'لطفاً عنوان، تاریخ و ساعت را وارد کنید.')
            return redirect('members:dashboard')
        
        event = Event.objects.create(
            title=title,
            jalali_date=jalali_date,
            time=time,
            short_description=short_description or '',
            capacity=capacity,
            status='upcoming',
            instructor_name=member.full_name,
            created_by=request.user,
            image=image,
        )
        
        messages.success(request, f'رویداد "{event.title}" با موفقیت ایجاد شد.')
        return redirect('members:dashboard')
    
    return redirect('members:dashboard')


@login_required
def delete_event(request, pk):
    """حذف رویداد"""
    if request.method != 'POST':
        return redirect('members:dashboard')

    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')

    event = get_object_or_404(Event, pk=pk)

    if event.created_by != request.user:
        messages.error(request, 'شما مجوز حذف این رویداد را ندارید.')
        return redirect('members:dashboard')

    event.delete()
    messages.success(request, 'رویداد با موفقیت حذف شد.')
    return redirect('members:dashboard')


@login_required
def upload_gallery(request):
    """بارگذاری تصویر در گالری"""
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        
        if not image:
            messages.error(request, 'لطفاً یک تصویر انتخاب کنید.')
            return redirect('members:dashboard')
        
        GalleryImage.objects.create(
            title=caption or "بدون عنوان",
            image=image,
            description=f"بارگذاری شده توسط {member.full_name}",
            uploaded_by=request.user
        )
        
        messages.success(request, 'تصویر با موفقیت بارگذاری شد.')
        return redirect('members:dashboard')
    
    return redirect('members:dashboard')


@login_required
def upload_resource(request):
    """بارگذاری منبع داخلی"""
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        file = request.FILES.get('file')
        
        if not title:
            messages.error(request, 'لطفاً عنوان منبع را وارد کنید.')
            return redirect('members:dashboard')
        
        InternalResource.objects.create(
            title=title,
            category=category or 'other',
            file=file,
            uploaded_by=request.user
        )
        
        messages.success(request, 'منبع با موفقیت بارگذاری شد.')
        return redirect('members:dashboard')
    
    return redirect('members:dashboard')


@login_required
def delete_resource(request, pk):
    """حذف منبع داخلی"""
    if request.method != "POST":
        return redirect("members:dashboard")

    member = check_member_access(request)
    if not member:
        return redirect("members:dashboard")

    resource = get_object_or_404(InternalResource, pk=pk)

    if resource.uploaded_by != request.user:
        messages.error(request, "شما مجوز حذف این منبع را ندارید.")
        return redirect("members:dashboard")

    resource.delete()
    messages.success(request, "منبع حذف شد.")
    return redirect("members:dashboard")


@login_required
def member_request_view(request):
    """ثبت درخواست عضویت"""
    if Member.objects.filter(user=request.user).exists():
        messages.warning(request, 'شما قبلاً عضو انجمن هستید.')
        return redirect('members:dashboard')
    
    if MemberRequest.objects.filter(user=request.user, status='pending').exists():
        messages.warning(request, 'شما قبلاً درخواست عضویت ثبت کرده‌اید.')
        return redirect('members:dashboard')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        committee_id = request.POST.get('committee')
        message_text = request.POST.get('message', '')
        
        if not student_id or not committee_id:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید.')
            return redirect('members:member_request')
        
        committee = get_object_or_404(Committee, id=committee_id)
        
        MemberRequest.objects.create(
            user=request.user,
            committee=committee,
            student_id=student_id,
            message=message_text,
            status='pending'
        )
        
        messages.success(request, 'درخواست عضویت شما با موفقیت ثبت شد.')
        return redirect('members:dashboard')
    
    committees = Committee.objects.all()
    return render(request, 'member_request.html', {'committees': committees})


@login_required
def gallery_delete(request, pk):
    """حذف تصویر از گالری"""
    if request.method != 'POST':
        return redirect('members:dashboard')

    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')

    image = get_object_or_404(GalleryImage, pk=pk)

    if image.uploaded_by != request.user and not request.user.is_staff:
        messages.error(request, 'شما مجوز حذف این تصویر را ندارید.')
        return redirect('members:dashboard')

    if image.image:
        image.image.delete(save=False)

    image.delete()
    messages.success(request, 'تصویر با موفقیت حذف شد.')
    return redirect('members:dashboard')


@login_required
def invite_professor(request):
    """دعوت از استاد (همه اعضا میتونن)"""
    member = check_member_access(request)
    if not member:
        return redirect("members:dashboard")

    if request.method == "POST":
        event_id = request.POST.get("event")
        professor_id = request.POST.get("professor")
        message = request.POST.get("message", "")

        if not event_id or not professor_id:
            messages.error(request, "لطفاً رویداد و استاد را انتخاب کنید.")
            return redirect("members:dashboard")

        event = get_object_or_404(Event, id=event_id)
        professor = get_object_or_404(User, id=professor_id)

        if not hasattr(professor, 'professor_profile'):
            messages.error(request, "کاربر انتخاب شده استاد نیست.")
            return redirect("members:dashboard")

        if EventInvitation.objects.filter(event=event, professor=professor).exists():
            messages.warning(request, "این استاد قبلاً دعوت شده.")
            return redirect("members:dashboard")

        EventInvitation.objects.create(
            event=event,
            professor=professor,
            role='instructor',
            message=message,
            created_by=request.user,
        )

        messages.success(request, f"دعوت‌نامه برای استاد {professor.get_full_name()} ارسال شد.")
        return redirect("members:dashboard")

    return redirect("members:dashboard")


# ==========================================
# ✅ ویوهای مدیریت مقالات (همه اعضا)
# ==========================================

@login_required
def approve_article(request, pk):
    """تأیید مقاله پیشنهادی"""
    if request.method != 'POST':
        return redirect('members:dashboard')
    
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    article = get_object_or_404(ProfessorArticle, pk=pk, status='submitted')
    
    article.status = 'approved'
    article.admin_feedback = request.POST.get('feedback', 'تأیید شد')
    article.save()
    
    messages.success(request, f'مقاله "{article.title}" با موفقیت تأیید شد.')
    return redirect('members:dashboard')


@login_required
def reject_article(request, pk):
    """رد مقاله پیشنهادی"""
    if request.method != 'POST':
        return redirect('members:dashboard')
    
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    article = get_object_or_404(ProfessorArticle, pk=pk, status='submitted')
    
    article.status = 'rejected'
    article.admin_feedback = request.POST.get('feedback', 'رد شد')
    article.save()
    
    messages.success(request, f'مقاله "{article.title}" رد شد.')
    return redirect('members:dashboard')


# ==========================================
# ✅ ویوهای مدیریت پیشنهادات رویداد (همه اعضا)
# ==========================================

@login_required
def approve_event_proposal(request, pk):
    """تأیید پیشنهاد رویداد"""
    if request.method != 'POST':
        return redirect('members:dashboard')
    
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    proposal = get_object_or_404(EventProposal, pk=pk, status='pending')
    
    proposal.status = 'approved'
    proposal.admin_feedback = request.POST.get('feedback', 'تأیید شد')
    proposal.save()
    
    messages.success(request, f'پیشنهاد رویداد "{proposal.title}" با موفقیت تأیید شد.')
    return redirect('members:dashboard')


@login_required
def reject_event_proposal(request, pk):
    """رد پیشنهاد رویداد"""
    if request.method != 'POST':
        return redirect('members:dashboard')
    
    member = check_member_access(request)
    if not member:
        return redirect('members:dashboard')
    
    proposal = get_object_or_404(EventProposal, pk=pk, status='pending')
    
    proposal.status = 'rejected'
    proposal.admin_feedback = request.POST.get('feedback', 'رد شد')
    proposal.save()
    
    messages.success(request, f'پیشنهاد رویداد "{proposal.title}" رد شد.')
    return redirect('members:dashboard')
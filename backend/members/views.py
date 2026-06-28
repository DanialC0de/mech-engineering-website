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
    # درخواست‌های عضویت (فقط برای مدیران)
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
        role='professor'  # اگر فیلد role در مدل User دارید
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

    try:
        current_member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید.')
        return redirect('members:dashboard')

    # فقط رئیس و نائب رئیس
    if current_member.role not in ['head', 'vice']:
        messages.error(request, 'شما مجوز رد درخواست را ندارید.')
        return redirect('members:dashboard')

    member_request = get_object_or_404(
        MemberRequest,
        pk=pk,
        status='pending'
    )

    member_request.status = 'rejected'
    member_request.save(update_fields=['status'])

    messages.success(
        request,
        'درخواست عضویت با موفقیت رد شد.'
    )
    if member_request.user == request.user:
        messages.error(request,"نمی‌توانید درخواست خودتان را رد کنید.")
    return redirect('members:dashboard')




@login_required
def create_event(request):
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید. امکان ایجاد رویداد وجود ندارد.')
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

    if request.method != 'POST':
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
    """بارگذاری تصویر در گالری (فقط برای اعضای انجمن)"""
    # چک کردن اینکه کاربر عضو هست
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید. امکان بارگذاری تصویر وجود ندارد.')
        return redirect('members:dashboard')
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        
        if not image:
            messages.error(request, 'لطفاً یک تصویر انتخاب کنید.')
            return redirect('members:dashboard')
        
        from website.models import GalleryItem
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
    """بارگذاری منبع داخلی (فقط برای اعضای انجمن)"""
    # چک کردن اینکه کاربر عضو هست
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید. امکان بارگذاری منبع وجود ندارد.')
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
    if request.method != "POST":
        return redirect("members:dashboard")

    resource = get_object_or_404(InternalResource, pk=pk)

    try:
        Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request,"شما عضو انجمن نیستید.")
        return redirect("members:dashboard")

    if resource.uploaded_by != request.user:
        messages.error(request,"شما مجوز حذف این منبع را ندارید.")
        return redirect("members:dashboard")

    resource.delete()

    messages.success(request,"منبع حذف شد.")

    return redirect("members:dashboard")


@login_required
def member_request_view(request):
    """ثبت درخواست عضویت"""
    
    # بررسی اینکه کاربر قبلاً عضو هست یا نه
    if Member.objects.filter(user=request.user).exists():
        messages.warning(request, 'شما قبلاً عضو انجمن هستید.')
        return redirect('members:dashboard')
    
    # بررسی اینکه کاربر قبلاً درخواست داده یا نه
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
        
        messages.success(request, 'درخواست عضویت شما با موفقیت ثبت شد. منتظر تأیید مدیر باشید.')
        return redirect('members:dashboard')
    
    committees = Committee.objects.all()
    return render(request, 'member_request.html', {'committees': committees})  # ← مسیر درسته


@login_required
def approve_request(request, pk):
    """تأیید درخواست عضویت"""
    if request.method != 'POST':
        messages.error(request, 'درخواست نامعتبر است.')
        return redirect('members:dashboard')

    try:
        current_member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید.')
        return redirect('members:dashboard')

    member_request = get_object_or_404(MemberRequest, pk=pk, status='pending')

    if Member.objects.filter(user=member_request.user).exists():
        messages.warning(request, 'این کاربر قبلاً عضو انجمن شده است.')
        member_request.status = 'rejected'
        member_request.save(update_fields=['status'])
        return redirect('members:dashboard')
    
    if Member.objects.filter(student_id=member_request.student_id).exists():
        messages.error(request, f'شماره دانشجویی "{member_request.student_id}" قبلاً ثبت شده است.')
        member_request.status = 'rejected'
        member_request.save(update_fields=['status'])
        return redirect('members:dashboard')

    try:
        member_request.status = "approved"
        member_request.save()
        
        member_request.status = 'approved'
        member_request.save(update_fields=['status'])
        
        messages.success(request, 'درخواست عضویت با موفقیت تأیید شد.')

    except Exception as e:
        messages.error(request, f'خطا در تأیید درخواست: {str(e)}')
        member_request.status = 'rejected'
        member_request.save(update_fields=['status'])
    
    return redirect('members:dashboard')


@login_required
def gallery_delete(request, pk):
    """حذف تصویر از گالری"""
    if request.method != 'POST':
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
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        messages.error(request, "شما عضو انجمن نیستید.")
        return redirect("members:dashboard")

    if member.role not in ["head", "vice"]:
        messages.error(request, "دسترسی ندارید.")
        return redirect("members:dashboard")

    if request.method == "POST":
        event_id = request.POST.get("event")
        professor_id = request.POST.get("professor")  # این ID کاربر است
        message = request.POST.get("message", "")

        event = get_object_or_404(Event, id=event_id)
        
        # ✅ استفاده از مدل User چون در اپ professor اینگونه تعریف شده
        professor = get_object_or_404(User, id=professor_id)

        # بررسی اینکه کاربر واقعاً استاد است
        if not hasattr(professor, 'professor_profile'):
            messages.error(request, "کاربر انتخاب شده استاد نیست.")
            return redirect("members:dashboard")

        # جلوگیری از تکراری
        if EventInvitation.objects.filter(event=event, professor=professor).exists():
            messages.warning(request, "این استاد قبلاً دعوت شده.")
            return redirect("members:dashboard")

        # ✅ ایجاد با مدل اپ professor
        EventInvitation.objects.create(
            event=event,
            professor=professor,  # ارسال مستقیم مدل User
            role='instructor',  # مقدار پیش‌فرض
            message=message,
            created_at=timezone.now()  # یا auto_now_add=True در مدل
        )

        messages.success(request, "دعوت با موفقیت ارسال شد.")
        return redirect("members:dashboard")

    return redirect("members:dashboard")
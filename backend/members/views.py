from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member, MemberRequest, Committee, InternalResource
from events.models import Event, Registration
from website.models import GalleryItem

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
        })
    
    # رویدادهای تحت مسئولیت کاربر (۳ تا برای داشبورد)
    my_events = Event.objects.filter(
        created_by=request.user
    )[:3]
    
    # همه رویدادهای کاربر برای صفحه مدیریت رویدادها
    all_my_events = Event.objects.filter(
        created_by=request.user
    )
    
    # درخواست‌های عضویت
    pending_requests = MemberRequest.objects.filter(status='pending')
    
    # اعضای انجمن
    members_list = Member.objects.filter(is_active=True)
    
    # منابع داخلی کاربر
    internal_resources = InternalResource.objects.filter(uploaded_by=request.user)
    
    # گالری تصاویر (از اپ website)
    
    gallery_items = GalleryItem.objects.all().order_by('-order')
    
    context = {
        'member': member,
        'pending_requests': pending_requests.count(),
        'member_requests': pending_requests,
        'members': members_list,
        'committees': Committee.objects.all(),
        'internal_resources': internal_resources,
        'my_events': my_events,
        'all_my_events': all_my_events,
        'gallery_items': gallery_items,
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
        capacity = request.POST.get('capacity', 0)
        image = request.FILES.get('image')
        
        if not title or not jalali_date or not time:
            messages.error(request, 'لطفاً عنوان، تاریخ و ساعت را وارد کنید.')
            return redirect('members:dashboard')
        
        # ✅ اصلاح شده - بدون created_by
        event = Event.objects.create(
            title=title,
            jalali_date=jalali_date,
            time=time,
            short_description=short_description or '',
            capacity=int(capacity) if capacity else 0,
            status='upcoming',
            instructor_name=member.full_name,
            created_by=request.user,
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
        GalleryItem.objects.create(
            media_type='image',
            image=image,
            caption_title=caption or 'تصویر بدون عنوان',
            caption_text=f'بارگذاری شده توسط {member.full_name}',
            order=0
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
    if request.method != 'POST':
        """حذف منبع داخلی (فقط uploader)"""
        resource = get_object_or_404(InternalResource, pk=pk)
        
        # چک کردن اینکه کاربر عضو هست
        try:
            Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            messages.error(request, 'شما عضو انجمن نیستید.')
            return redirect('members:dashboard')
        
        # چک کردن مجوز حذف
        if resource.uploaded_by != request.user:
            messages.error(request, 'شما مجوز حذف این منبع را ندارید.')
            return redirect('members:dashboard')
        
        resource.delete()
        messages.success(request, 'منبع با موفقیت حذف شد.')
    return redirect('members:dashboard')


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
        Member.objects.create(
            user=member_request.user,
            student_id=member_request.student_id,
            committee=member_request.committee,
            role='member',
            is_active=True
        )
        
        member_request.status = 'approved'
        member_request.save(update_fields=['status'])
        
        messages.success(request, 'درخواست عضویت با موفقیت تأیید شد.')

    except Exception as e:
        messages.error(request, f'خطا در تأیید درخواست: {str(e)}')
        member_request.status = 'rejected'
        member_request.save(update_fields=['status'])
    
    return redirect('members:dashboard')
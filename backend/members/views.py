from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member, MemberRequest, Committee, InternalResource, GalleryImage
from events.models import Event

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
            'gallery_images': [],
        })
    
    # رویدادهای تحت مسئولیت کاربر
    my_events = Event.objects.filter(
        Q(instructor_name__icontains=member.full_name) | 
        Q(created_by=request.user)
    )[:3]
    
    all_my_events = Event.objects.filter(
        Q(instructor_name__icontains=member.full_name) | 
        Q(created_by=request.user)
    )
    
    pending_requests = MemberRequest.objects.filter(status='pending')
    members_list = Member.objects.filter(is_active=True)
    internal_resources = InternalResource.objects.filter(uploaded_by=request.user)
    gallery_images = GalleryImage.objects.all()[:20]
    context = {
        'member': member,
        'pending_requests': pending_requests.count(),
        'member_requests': pending_requests,
        'members': members_list,
        'committees': Committee.objects.all(),
        'internal_resources': internal_resources,
        'my_events': my_events,
        'all_my_events': all_my_events,
        'gallery_images': gallery_images, 
    }
    return render(request, 'member.html', context)  # ← مسیر درسته


@login_required
def approve_request(request, pk):
    """تأیید درخواست عضویت"""
    try:
        current_member = Member.objects.get(user=request.user)
        if current_member.role not in ['head', 'vice']:
            messages.error(request, 'شما مجوز این کار را ندارید.')
            return redirect('members:dashboard')
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید.')
        return redirect('members:dashboard')
    
    member_request = get_object_or_404(MemberRequest, pk=pk)
    member_request.status = 'approved'
    member_request.save()
    
    Member.objects.create(
        user=member_request.user,
        student_id=member_request.student_id,
        committee=member_request.committee,
        role='member',
        is_active=True
    )
    
    messages.success(request, 'درخواست عضویت تأیید شد.')
    return redirect('members:dashboard')


@login_required
def reject_request(request, pk):
    """رد درخواست عضویت"""
    try:
        current_member = Member.objects.get(user=request.user)
        if current_member.role not in ['head', 'vice']:
            messages.error(request, 'شما مجوز این کار را ندارید.')
            return redirect('members:dashboard')
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید.')
        return redirect('members:dashboard')
    
    member_request = get_object_or_404(MemberRequest, pk=pk)
    member_request.status = 'rejected'
    member_request.save()
    
    messages.success(request, 'درخواست عضویت رد شد.')
    return redirect('members:dashboard')


@login_required
def create_event(request):
    """ایجاد رویداد جدید توسط عضو انجمن"""
    if request.method == 'POST':
        title = request.POST.get('title')
        jalali_date = request.POST.get('date')
        time = request.POST.get('time')
        short_description = request.POST.get('short_description')
        capacity = request.POST.get('capacity', 0)
        image = request.FILES.get('image') 

        if not title or not jalali_date or not time:
            messages.error(request, 'لطفاً همه فیلدهای ضروری را پر کنید.')
            return redirect('members:dashboard')
        
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            messages.error(request, 'شما عضو انجمن نیستید.')
            return redirect('members:dashboard')
        
        event = Event.objects.create(
            title=title,
            jalali_date=jalali_date,
            time=time,
            short_description=short_description or '',
            capacity=int(capacity) if capacity else 0,
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
    """حذف رویداد توسط عضو انجمن"""
    event = get_object_or_404(Event, pk=pk)
    
    try:
        member = Member.objects.get(user=request.user)
        if event.instructor_name != member.full_name:
            messages.error(request, 'شما مجوز حذف این رویداد را ندارید.')
            return redirect('members:dashboard')
    except Member.DoesNotExist:
        messages.error(request, 'شما عضو انجمن نیستید.')
        return redirect('members:dashboard')
    
    event.delete()
    messages.success(request, 'رویداد با موفقیت حذف شد.')
    return redirect('members:dashboard')



@login_required
def gallery_upload(request):
    """آپلود تصویر جدید در گالری"""
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description', '')
        
        if not title or not image:
            messages.error(request, 'لطفاً عنوان و تصویر را وارد کنید.')
            return redirect('members:dashboard')
        
        if not image.content_type.startswith('image/'):
            messages.error(request, 'لطفاً فقط فایل تصویری آپلود کنید.')
            return redirect('members:dashboard')
        
        # ذخیره در دیتابیس
        try:
            GalleryImage.objects.create(
                title=title,
                image=image,
                description=description,
                uploaded_by=request.user
            )
            messages.success(request, '✅ تصویر با موفقیت آپلود شد.')
        except Exception as e:
            messages.error(request, f'خطا در آپلود تصویر: {str(e)}')
        
        return redirect('members:dashboard')
    
    return redirect('members:dashboard')
@login_required
def gallery_delete(request, pk):
    """حذف تصویر از گالری"""
    image = get_object_or_404(GalleryImage, pk=pk)
    
    # فقط کسی که آپلود کرده یا ادمین میتونه حذف کنه
    if image.uploaded_by != request.user and not request.user.is_staff:
        messages.error(request, 'شما مجوز حذف این تصویر را ندارید.')
        return redirect('members:dashboard')
    
    image.delete()
    messages.success(request, 'تصویر با موفقیت حذف شد.')
    return redirect('members:dashboard')
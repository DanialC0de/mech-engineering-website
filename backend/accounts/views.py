from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import OTP
from .sms_service import send_otp_sms
from students.models import StudentProfile
from .decorators import role_required  # 🔥 دکوریتوری که ساختی

User = get_user_model()

# ============================================
# توابع کمکی
# ============================================

def normalize_phone(phone):
    """تبدیل اعداد فارسی به انگلیسی"""
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    for p, e in zip(persian, english):
        phone = phone.replace(p, e)
    return phone


def normalize_digits(value):
    """تبدیل اعداد فارسی و عربی به انگلیسی"""
    translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789"
    )
    return (value or "").translate(translation)


# ============================================
# صفحات HTML
# ============================================

def login_page(request):
    """صفحه ورود"""
    return render(request, "login.html")


def register_page(request):
    """صفحه تکمیل ثبت‌نام دانشجو پس از تأیید شماره موبایل"""
    phone = request.session.get("register_phone")
    if not phone:
        return redirect("login_page")

    masked_phone = f"{phone[:4]}***{phone[-4:]}" if len(phone) == 11 else phone
    return render(request, "register.html", {"masked_phone": masked_phone})


def verify_page(request):
    """صفحه تایید کد"""
    return render(request, "verify.html")


# ============================================
# ثبت‌نام کاربر (با OTP)
# ============================================

@require_POST
def register_view(request):
    """
    ثبت‌نام دانشجو با شماره موبایلی که قبلاً با OTP تأیید شده است.
    """
    phone = request.session.get("register_phone")
    if not phone:
        return JsonResponse({
            "status": "error",
            "message": "شماره موبایل تأیید نشده است. لطفاً دوباره وارد شوید.",
            "redirect": reverse("login_page"),
        }, status=403)

    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    student_id = normalize_digits(request.POST.get("student_id", "").strip())
    major = request.POST.get("major", "").strip()
    level = request.POST.get("level", "").strip()
    entry_year = normalize_digits(request.POST.get("entry_year", "").strip())
    term = request.POST.get("term", "").strip()
    interest = request.POST.get("interest", "").strip()
    bio = request.POST.get("bio", "").strip()

    required_fields = {
        "نام": first_name,
        "نام خانوادگی": last_name,
        "شماره دانشجویی": student_id,
        "رشته تحصیلی": major,
        "مقطع تحصیلی": level,
        "سال ورود": entry_year,
    }
    missing_fields = [label for label, value in required_fields.items() if not value]
    if missing_fields:
        return JsonResponse({
            "status": "error",
            "message": f"فیلدهای الزامی را کامل کنید: {('، ').join(missing_fields)}"
        }, status=400)

    if not student_id.isdigit() or len(student_id) != 8:
        return JsonResponse({
            "status": "error",
            "message": "شماره دانشجویی باید ۸ رقمی باشد"
        }, status=400)

    try:
        parsed_entry_year = int(entry_year)
    except ValueError:
        return JsonResponse({
            "status": "error",
            "message": "سال ورود باید عدد باشد"
        }, status=400)

    if parsed_entry_year < 1390 or parsed_entry_year > 1410:
        return JsonResponse({
            "status": "error",
            "message": "سال ورود باید بین ۱۳۹۰ تا ۱۴۱۰ باشد"
        }, status=400)

    if User.objects.filter(phone_number=phone).exists():
        return JsonResponse({
            "status": "error",
            "message": "این شماره موبایل قبلاً ثبت شده است",
            "redirect": reverse("login_page"),
        }, status=400)

    if StudentProfile.objects.filter(student_id=student_id).exists():
        return JsonResponse({
            "status": "error",
            "message": "این شماره دانشجویی قبلاً ثبت شده است"
        }, status=400)

    try:
        with transaction.atomic():
            user = User(
                phone_number=phone,
                username=student_id,
                first_name=first_name,
                last_name=last_name,
                role="student"
            )
            user.set_unusable_password()
            user.save()

            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                major=major,
                level=level,
                entry_year=parsed_entry_year,
                term=term,
                interest=interest,
                bio=bio
            )

        login(request, user)
        request.session.pop("register_phone", None)

        return JsonResponse({
            "status": "ok",
            "redirect": reverse("students:panel"),
            "message": "ثبت‌نام دانشجو با موفقیت انجام شد"
        })

    except IntegrityError:
        return JsonResponse({
            "status": "error",
            "message": "اطلاعات واردشده قبلاً ثبت شده است"
        }, status=400)


# ============================================
# ارسال کد OTP
# ============================================

@csrf_exempt
def send_otp_view(request):
    """ارسال کد تایید به شماره موبایل"""
    
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "درخواست نامعتبر"
        }, status=405)

    try:
        data = json.loads(request.body)
        phone = data.get("phone", "").strip()
        phone = normalize_phone(phone)
    except Exception as e:
        print("JSON ERROR:", e)
        return JsonResponse({
            "status": "error",
            "message": "اطلاعات نامعتبر است"
        }, status=400)

    print("PHONE =", phone)

    if not phone:
        return JsonResponse({
            "status": "error",
            "message": "شماره موبایل وارد نشده است"
        }, status=400)

    # حذف کدهای قبلی استفاده نشده
    OTP.objects.filter(
        phone_number=phone,
        is_used=False
    ).delete()

    # ساخت کد جدید
    code = OTP.generate_code()
    
    OTP.objects.create(
        phone_number=phone,
        code=code
    )

    # ارسال پیامک
    try:
        result = send_otp_sms(phone, code)
        print("SMS RESULT =", result)

        if not result:
            return JsonResponse({
                "status": "error",
                "message": "خطا در ارسال پیامک"
            }, status=500)
    except Exception as e:
        print("SMS ERROR =", e)
        return JsonResponse({
            "status": "error",
            "message": "خطا در ارسال پیامک"
        }, status=500)

    # ذخیره شماره در سشن برای تایید بعدی
    request.session["verify_phone"] = phone

    return JsonResponse({
        "status": "sent",
        "message": "کد تایید ارسال شد"
    })


# ============================================
# تایید کد OTP
# ============================================

@csrf_exempt
def verify_otp_view(request):
    """تایید کد OTP و ورود کاربر"""
    
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "متد نامعتبر"
        }, status=405)

    try:
        data = json.loads(request.body)
        code = data.get("code", "").strip()
    except:
        return JsonResponse({
            "status": "error",
            "message": "اطلاعات نامعتبر است"
        }, status=400)

    phone = request.session.get("verify_phone")

    if not phone:
        return JsonResponse({
            "status": "error",
            "message": "زمان نشست شما تمام شده است"
        }, status=400)

    # نرمال سازی کد (تبدیل فارسی به انگلیسی)
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    for p, e in zip(persian, english):
        code = code.replace(p, e)

    # پیدا کردن کد در دیتابیس
    otp = OTP.objects.filter(
        phone_number=phone,
        code=code,
        is_used=False
    ).first()

    if not otp:
        return JsonResponse({
            "status": "error",
            "message": "کد وارد شده صحیح نیست"
        }, status=400)

    # بررسی انقضا (۲ دقیقه)
    if timezone.now() > otp.created_at + timezone.timedelta(minutes=2):
        return JsonResponse({
            "status": "error",
            "message": "کد منقضی شده است"
        }, status=400)

    # تایید کد
    otp.is_used = True
    otp.save()
    request.session.pop("verify_phone", None)

    # پیدا کردن کاربر
    user = User.objects.filter(phone_number=phone).first()

    if user:
        # کاربر وجود دارد → ورود
        login(request, user)
        
        # 🔥 تعیین مسیر هدایت بر اساس نقش
        redirect_url = "/panel/student/"  # پیش‌فرض: دانشجو
        if user.role == "professor":
            redirect_url = "/panel/professor/"
        elif user.role == "member":  # 🔥 عضو انجمن
            redirect_url = "/members/"
        
        return JsonResponse({
            "status": "success",
            "redirect": redirect_url
        })
    else:
        # کاربر وجود ندارد → برو به صفحه ثبت‌نام
        request.session["register_phone"] = phone
        return JsonResponse({
            "status": "register",
            "redirect": "/accounts/register/"
        })


# ============================================
# ورود با شماره موبایل (صفحه)
# ============================================

def login_view(request):
    """صفحه ورود"""
    return render(request, "login.html")


# ============================================
# خروج از حساب کاربری
# ============================================

def logout_view(request):
    """خروج کاربر از سیستم"""
    logout(request)
    return redirect('login_page')


# ============================================
# 🔥 پنل‌های کاربری با محدودیت دسترسی
# ============================================

@login_required
@role_required(['student'])  # فقط دانشجوها و سوپرادمین
def student_panel(request):
    """
    پنل دانشجو
    آدرس: /panel/student/
    """
    # دریافت پروفایل دانشجو
    try:
        profile = request.user.student_profile
    except:
        profile = None
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    
    return render(request, 'panel/student_dashboard.html', context)


@login_required
@role_required(['professor'])  # فقط استادها و سوپرادمین
def professor_panel(request):
    """
    پنل استاد
    آدرس: /panel/professor/
    """
    # دریافت پروفایل استاد
    try:
        professor = request.user.professor_profile
    except:
        professor = None
    
    context = {
        'user': request.user,
        'professor': professor,
    }
    
    return render(request, 'professor.html', context)


@login_required
@role_required(['member'])  # فقط اعضای انجمن و سوپرادمین
def member_panel(request):
    """
    پنل عضو انجمن
    آدرس: /members/
    """
    context = {
        'user': request.user,
    }
    
    return render(request, 'members_dashboard.html', context)

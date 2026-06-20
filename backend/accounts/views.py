from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone

from .models import OTP
from .sms_service import send_otp_sms
from students.models import StudentProfile  # ✅ اضافه شد

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


# ============================================
# صفحات HTML
# ============================================

def login_page(request):
    """صفحه ورود"""
    return render(request, "login.html")


def register_page(request):
    """صفحه ثبت‌نام"""
    return render(request, "register.html")


def verify_page(request):
    """صفحه تایید کد"""
    return render(request, "verify.html")


# ============================================
# ثبت‌نام کاربر (با OTP)
# ============================================

@csrf_exempt
def register_view(request):
    """
    ثبت‌نام کاربر جدید با شماره موبایل و OTP
    بعد از ثبت‌نام، StudentProfile هم ساخته میشه
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "متد اشتباه"}, status=405)

    # دریافت اطلاعات از فرم
    phone = request.POST.get("phone")
    username = request.POST.get("username")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    
    # اطلاعات StudentProfile
    student_id = request.POST.get("student_id")
    major = request.POST.get("major")
    level = request.POST.get("level") or request.POST.get("degree")
    entry_year = request.POST.get("entry_year")
    term = request.POST.get("term")
    committee = request.POST.get("committee", "")
    interest = request.POST.get("interest", "")
    bio = request.POST.get("bio", "")

    # اعتبارسنجی اولیه
    if not phone or not username:
        return JsonResponse({
            "status": "error",
            "message": "شماره موبایل و نام کاربری الزامی است"
        }, status=400)

    # بررسی تکراری نبودن شماره موبایل
    if User.objects.filter(phone_number=phone).exists():
        return JsonResponse({
            "status": "error",
            "message": "این شماره موبایل قبلاً ثبت شده است"
        }, status=400)

    # بررسی تکراری نبودن نام کاربری
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": "error",
            "message": "این نام کاربری قبلاً ثبت شده است"
        }, status=400)

    try:
        # ============================================
        # 1. ساخت کاربر جدید
        # ============================================
        user = User.objects.create(
            phone_number=phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            role="student"  # نقش پیش‌فرض: دانشجو
        )
        user.set_unusable_password()  # چون با OTP وارد میشه
        user.save()
        
        print(f"✅ کاربر {username} ساخته شد")

        # ============================================
        # 2. ساخت پروفایل دانشجو
        # ============================================
        student_profile = StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            major=major,
            level=level,
            entry_year=int(entry_year) if entry_year else None,
            term=term,
            committee=committee,
            interest=interest,
            bio=bio
        )
        
        print(f"✅ پروفایل دانشجو برای {username} ساخته شد")
        print(f"   شماره دانشجویی: {student_profile.student_id}")
        print(f"   رشته: {student_profile.major}")

        # ============================================
        # 3. ورود خودکار کاربر
        # ============================================
        login(request, user)

        # ============================================
        # 4. پاسخ موفق
        # ============================================
        return JsonResponse({
            "status": "ok",
            "redirect": "/panel/student/",
            "message": "ثبت‌نام با موفقیت انجام شد"
        })

    except Exception as e:
        # اگر خطایی رخ داد، کاربر رو پاک کن (Rollback)
        print(f"❌ خطا در ثبت‌نام: {e}")
        
        # اگر کاربر ساخته شده بود، حذفش کن
        if 'user' in locals():
            user.delete()
            print(f"🗑️ کاربر {username} به دلیل خطا حذف شد")
        
        return JsonResponse({
            "status": "error",
            "message": f"خطا در ثبت‌نام: {str(e)}"
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
        
        # تعیین مسیر هدایت بر اساس نقش
        redirect_url = "/panel/student/"
        if user.role == "professor":
            redirect_url = "/panel/professor/"
        
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
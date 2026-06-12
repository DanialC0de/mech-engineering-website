from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings

from .models import OTP
from .sms_service import send_otp_sms

User = get_user_model()

def normalize_phone(phone):
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"

    for p, e in zip(persian, english):
        phone = phone.replace(p, e)

    return phone

# ---------- صفحات ----------

def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def verify_page(request):
    return render(request, "verify.html")


# ---------- ثبت نام ----------

def register_view(request):

    phone = request.session.get("register_phone")

    if not phone:
        return redirect("/accounts/login/")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()

        if not username:
            return render(request, "register.html", {
                "error": "نام کاربری الزامی است"
            })

        role = "student"

        if phone in getattr(settings, "PROFESSOR_PHONES", []):
            role = "professor"

        user = User.objects.create(
            phone_number=phone,
            username=username,
            role=role,
        )

        user.set_unusable_password()
        user.save()

        login(request, user)

        del request.session["register_phone"]

        if role == "professor":
            return redirect("/panel/professor/")
        else:
            return redirect("/panel/student/")

    return render(request, "register.html")

# ---------- ارسال OTP ----------
import json
from django.http import JsonResponse
@csrf_exempt
def send_otp_view(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "درخواست نامعتبر"
        })

    try:
        data = json.loads(request.body)
        phone = data.get("phone", "").strip()
        phone = normalize_phone(phone)


    except Exception as e:

        print("JSON ERROR:", e)

        return JsonResponse({
            "status": "error",
            "message": "اطلاعات نامعتبر است"
        })

    print("PHONE =", phone)

    if not phone:
        return JsonResponse({
            "status": "error",
            "message": "شماره موبایل وارد نشده است"
        })

    # حذف کدهای قبلی
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

    try:

        result = send_otp_sms(phone, code)

        print("SMS RESULT =", result)

        if not result:
            return JsonResponse({
                "status": "error",
                "message": "خطا در ارسال پیامک"
            })

    except Exception as e:

        print("SMS ERROR =", e)

        return JsonResponse({
            "status": "error",
            "message": "خطا در ارسال پیامک"
        })

    request.session["verify_phone"] = phone

    return JsonResponse({
        "status": "sent"
    })

# ---------- تایید OTP ----------
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import OTP

User = get_user_model()


def verify_otp_view(request):

    if request.method != "POST":
        return render(request, "verify.html")

    # گرفتن کد
    code = request.POST.get("code", "").strip()

    # نرمال سازی اعداد فارسی به انگلیسی
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    for p, e in zip(persian, english):
        code = code.replace(p, e)

    # گرفتن شماره از session
    phone = request.session.get("verify_phone")

    print("SESSION PHONE =", phone)
    print("ENTERED CODE =", code)

    if not phone:
        return render(request, "verify.html", {
            "error": "ابتدا شماره موبایل را وارد کنید"
        })

    phone = phone.strip()

    # پیدا کردن آخرین OTP معتبر
    otp = OTP.objects.filter(
        phone_number=phone,
        code=code,
        is_used=False
    ).order_by("-created_at").first()

    print("OTP FOUND =", otp)

    if not otp:
        return render(request, "verify.html", {
            "error": "کد وارد شده صحیح نیست"
        })

    # بررسی انقضا (اگر متد is_expired داری استفاده کن)
    if hasattr(otp, "is_expired"):
        if otp.is_expired():
            return render(request, "verify.html", {
                "error": "کد منقضی شده است"
            })
    else:
        # اگر متد نداری این روش را استفاده کن (۲ دقیقه اعتبار)
        if timezone.now() > otp.created_at + timezone.timedelta(minutes=2):
            return render(request, "verify.html", {
                "error": "کد منقضی شده است"
            })

    # علامت استفاده شده
    otp.is_used = True
    otp.save()

    # پاک کردن session otp
    request.session.pop("verify_phone", None)

    # بررسی وجود کاربر
    user = User.objects.filter(phone_number=phone).first()

    if user:
        # کاربر قبلاً ثبت نام کرده
        login(request, user)

        # هدایت بر اساس نقش
        if user.role == "professor":
            return redirect("/panel/professor/")
        elif user.role == "student":
            return redirect("/panel/student/")
        else:
            return redirect("/panel/")

    else:
        # کاربر جدید → ثبت نام
        request.session["register_phone"] = phone
        return redirect("/accounts/register/")


# ---------- لاگین ----------

def login_view(request):
    return render(request, "login.html")
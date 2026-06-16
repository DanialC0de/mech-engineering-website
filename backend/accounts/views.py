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
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth import get_user_model

User = get_user_model()

def register_view(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "متد اشتباه"}, status=405)

    phone = request.POST.get("phone")
    username = request.POST.get("username")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    if not phone or not username:
        return JsonResponse({"status": "error", "message": "اطلاعات ناقص است"}, status=400)

    user = User.objects.create(
        phone_number=phone,
        username=username,
        first_name=first_name,
        last_name=last_name,
        role="student"
    )

    user.set_unusable_password()
    user.save()

    login(request, user)

    return JsonResponse({
        "status": "ok",
        "redirect": "/panel/student/"
    })
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
@csrf_exempt
def verify_otp_view(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "متد نامعتبر"}, status=405)

    data = json.loads(request.body)
    code = data.get("code", "").strip()
    phone = request.session.get("verify_phone")

    if not phone:
        return JsonResponse({"status": "error", "message": "زمان نشست شما تمام شده است"}, status=400)

    # نرمال سازی کد
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    for p, e in zip(persian, english):
        code = code.replace(p, e)

    otp = OTP.objects.filter(phone_number=phone, code=code, is_used=False).first()

    if not otp:
        return JsonResponse({"status": "error", "message": "کد وارد شده صحیح نیست"}, status=400)

    # بررسی انقضا
    if timezone.now() > otp.created_at + timezone.timedelta(minutes=2):
        return JsonResponse({"status": "error", "message": "کد منقضی شده است"}, status=400)

    otp.is_used = True
    otp.save()
    request.session.pop("verify_phone", None)

    user = User.objects.filter(phone_number=phone).first()

    if user:
        login(request, user)
        # تعیین مسیر هدایت بر اساس نقش
        redirect_url = "/panel/student/"
        if user.role == "professor":
            redirect_url = "/panel/professor/"
        
        return JsonResponse({"status": "success", "redirect": redirect_url})
    else:
        request.session["register_phone"] = phone
        return JsonResponse({"status": "register", "redirect": "/accounts/register/"})
# ---------- لاگین ----------

def login_view(request):
    return render(request, "login.html")
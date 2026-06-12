from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Accounts app is connected!")
from .sms_service import send_otp_sms

import random
from django.http import HttpResponse
from .sms_service import send_otp_sms

def sms_test(request):
    # تولید یک کد ۴ رقمی تصادفی
    random_otp = random.randint(1000, 9999)
    
    # ارسال پیامک با کد تصادفی
    response = send_otp_sms("09137614011", random_otp)
    
    return HttpResponse(f"Status Code: {response.status_code} - Message: {response.text}")

import requests
from django.conf import settings

BASE_URL = "https://edge.ippanel.com/v1"


def send_otp_sms(phone, code_value):
    url = f"{BASE_URL}/api/send"

    payload = {
        "sending_type": "pattern",
        "from_number": settings.IPPANEL_SENDER,
        "code": settings.IPPANEL_PATTERN_CODE,
        "recipients": [phone],
        "params": {
            "code": str(code_value)
        }
    }

    headers = {
        "Authorization": settings.IPPANEL_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    return response

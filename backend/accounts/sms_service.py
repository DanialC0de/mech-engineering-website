import requests
from django.conf import settings

BASE_URL = "https://edge.ippanel.com/v1/api/send"


def send_otp_sms(phone, code_value):

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

    try:
        response = requests.post(
            BASE_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print("SMS STATUS:", response.status_code)
        print("SMS RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        print("SMS ERROR:", e)
        return None

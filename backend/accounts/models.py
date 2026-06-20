# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("student", "دانشجو"),      # مقدار دیتابیس -> نمایش در ادمین
        ("professor", "استاد"),
        ("member", "عضو انجمن"),    # ✅ اضافه شد
    )

    phone_number = models.CharField(max_length=15, unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.phone_number}"


class OTP(models.Model):

    phone_number = models.CharField(max_length=15)

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    is_used = models.BooleanField(default=False)

    def is_expired(self):
        """OTP expires after 2 minutes"""
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

    @staticmethod
    def generate_code():
        """Generate 6 digit OTP"""
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
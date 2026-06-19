from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # تمام مسیرهای لاگین و ثبت‌نام اینجا مدیریت می‌شود
    path('', include('website.urls')),
    path('events/', include('events.urls')),  # اپ رویداده
]

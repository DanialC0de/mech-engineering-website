from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ===== صفحات اصلی =====
    path('', views.home, name='home'),
    
    # ===== اخبار =====
    # path('news/', views.all_news, name='all_news'),
    # path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # ===== رویدادها =====
    path('events/', views.all_events, name='all_events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/register/', views.register_event, name='register_event'),
    path('events/<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),
    
    # ===== منابع علمی =====
    path('resources/', views.all_resources, name='all_resources'),
    path('resources/<int:pk>/download/', views.download_resource, name='download_resource'),
    
    # ===== افتخارات =====
    path('honors/', views.honors, name='honors'),
    
    # ===== صفحات اطلاعاتی =====
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('industry/', views.industry, name='industry'),
    
    # ===== احراز هویت =====
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('verify/', views.verify_view, name='verify'),
    path('student/', views.student_view, name='student'),
    
    # ===== پنل کاربری =====
    path('dashboard/', views.user_dashboard, name='dashboard'),
]

# تنظیمات برای فایل‌های رسانه‌ای در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.all_news, name='all_news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('events/', views.all_events, name='all_events'),
    path('resources/', views.all_resources, name='all_resources'),
    path('resource/<int:pk>/download/', views.download_resource, name='download_resource'),
    path('about/', views.about, name='about'),
    path('honors/', views.honors, name='honors'),
    path('contact/', views.contact, name='contact'),
    path('industry/', views.industry, name='industry'),
    
    # اضافه کردن این سه خط برای احراز هویت
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # اگر ویو register داری
]
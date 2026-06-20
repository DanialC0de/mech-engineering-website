# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # صفحه اصلی پنل دانشجو
    path('', views.student_panel, name='panel'),
    
    # API ها برای ارتباط با فرانت‌اند
    path('api/dashboard/', views.get_dashboard_data, name='dashboard_data'),
    path('api/events/', views.get_events_list, name='events_list'),
    path('api/events/<int:event_id>/register/', views.register_event, name='register_event'),
    path('api/registrations/<int:registration_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('api/resources/', views.get_resources_list, name='resources_list'),
    path('api/resources/<int:resource_id>/download/', views.download_resource, name='download_resource'),
    path('api/profile/', views.get_profile_data, name='profile_data'),
    path('api/change-password/', views.change_password, name='change_password'),
]
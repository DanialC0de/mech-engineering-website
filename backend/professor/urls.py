# professor/urls.py
from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    # صفحه اصلی پنل استاد
    path('', views.professor_panel, name='panel'),
    
    # API ها برای ارتباط با فرانت‌اند
    path('api/dashboard/', views.get_dashboard_data, name='dashboard_data'),
    path('api/events/', views.get_events_list, name='events_list'),
    path('api/invitations/<int:invitation_id>/respond/', views.respond_to_invitation, name='respond_invitation'),
    path('api/profile/', views.get_profile_data, name='profile_data'),
    path('api/profile/update/', views.update_profile_data, name='update_profile_data'),
    path('api/change-password/', views.change_password, name='change_password'),
]

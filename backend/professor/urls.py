from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [

    # صفحه اصلی پنل استاد
    path(
        '',
        views.professor_panel,
        name='panel'
    ),

    # داشبورد
    path(
        'api/dashboard/',
        views.get_dashboard_data,
        name='dashboard_data'
    ),

    # دعوتنامه‌ها
    path(
        'api/invitations/',
        views.get_invitations_list,
        name='invitations_list'
    ),

    path(
        'api/invitations/<int:invitation_id>/respond/',
        views.respond_to_invitation,
        name='respond_invitation'
    ),

    # ارسال دعوتنامه توسط سوپریوزر
    path(
        'api/admin/send-invitation/',
        views.send_event_invitation,
        name='send_event_invitation'
    ),

    # رویدادها
    path(
        'api/events/',
        views.get_events_list,
        name='events_list'
    ),

    path(
        'api/events/propose/',
        views.propose_event,
        name='propose_event'
    ),

    # منابع علمی سایت (Resource)
    path(
        'api/resources/',
        views.get_resources_list,
        name='resources_list'
    ),

    # مقالات پیشنهادی استاد
    path(
        'api/articles/',
        views.get_articles_list,
        name='articles_list'
    ),

    path(
        'api/articles/create/',
        views.create_article,
        name='create_article'
    ),

    path(
        'api/articles/upload/',
        views.create_article,
        name='upload_article'
    ),

    path(
        'api/articles/<int:article_id>/delete/',
        views.delete_article,
        name='delete_article'
    ),

    # پروفایل
    path(
        'api/profile/',
        views.get_profile_data,
        name='profile_data'
    ),

    path(
        'api/profile/update/',
        views.update_profile_data,
        name='update_profile_data'
    ),

    path(
        'api/change-password/',
        views.change_password,
        name='change_password'
    ),
]
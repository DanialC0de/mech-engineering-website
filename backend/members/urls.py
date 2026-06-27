from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_dashboard, name='dashboard'),
    path('request/<int:pk>/approve/', views.approve_request, name='approve_request'),
    path('request/<int:pk>/reject/', views.reject_request, name='reject_request'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),
     path('gallery/upload/', views.upload_gallery, name='upload_gallery'),
    path('gallery/delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),
    path('resource/upload/', views.upload_resource, name='upload_resource'),
]

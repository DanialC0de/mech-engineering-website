from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='all_events'),              
    path('<int:pk>/', views.event_detail, name='event_detail'), 
    path('<int:pk>/register/', views.register_event, name='register_event'), 
    path('<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'), 
]
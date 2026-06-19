from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='list'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('<int:pk>/register/', views.register_event, name='register'),
    path('<int:pk>/cancel/', views.cancel_registration, name='cancel'),
]
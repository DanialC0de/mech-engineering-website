from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_news, name='all_news'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
]
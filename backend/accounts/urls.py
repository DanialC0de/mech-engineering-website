from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path("sms-test/", views.sms_test, name="sms_test"),
]

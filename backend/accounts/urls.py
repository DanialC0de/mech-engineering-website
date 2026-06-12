from django.urls import path
from . import views

urlpatterns = [

    # صفحات
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("verify/", views.verify_page, name="verify_page"),

    # API ها
    path("login-user/", views.login_view, name="login_user"),
    path("register-user/", views.register_view, name="register_user"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("send-otp/", views.send_otp_view, name="send_otp"),


]

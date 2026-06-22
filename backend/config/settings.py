from pathlib import Path
import os

# مسیر اصلی پروژه (backend)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-rc16xch(n6qz=#5=m8@p!x1k@&2s-g6cvkz^8#o1hn-p@76cje'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'events',
    'accounts',
    'news',
    'members',
    'students',
    'professor',  # اپ استاد اضافه شد
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fa-ir'  # تغییر به فارسی
TIME_ZONE = 'Asia/Tehran'  # تغییر به ایران
USE_I18N = True
USE_TZ = True

# تنظیمات فایل‌های استاتیک (CSS/JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# تنظیمات فایل‌های مدیا (آپلود فایل)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# تنظیمات SMS
IPPANEL_API_KEY = "YTIxMWJhMzQtNjViMS00ZTA2LWI0MTEtMWYxODkwZTM4NjEyZDJiN2JhY2YxYmNkM2MyZTViNDcxMDAwMGY5MjMzZmQ="
IPPANEL_PATTERN_CODE = "dj3v6rdzpofzk73"
IPPANEL_SENDER = "+983000505"

# اساتید
PROFESSOR_PHONES = [
    "09121234567",
    "09123334455",
]

# تنظیمات لاگین
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

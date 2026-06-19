from pathlib import Path

# مسیر اصلی پروژه (backend)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-rc16xch(n6qz=#5=m8@p!x1k@&2s-g6cvkz^8#o1hn-p@76cje'
DEBUG = True
ALLOWED_HOSTS = ['*'] # اضافه شد برای جلوگیری از خطا در اجرا

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
        'DIRS': [BASE_DIR / 'templates'], # اصلاح شد (خطای تمپلیت اینجا حل می‌شود)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
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

AUTH_USER_MODEL = 'accounts.CustomUser' # اصلاح شد (فقط یک بار تعریف شد)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# تنظیمات فایل‌های استاتیک (CSS/JS)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # اضافه شد برای شناسایی فایل‌های CSS و JS

# تنظیمات SMS
IPPANEL_API_KEY = "your-new-key"
IPPANEL_PATTERN_CODE = ""
IPPANEL_SENDER = ""

# اساتید
PROFESSOR_PHONES = [
    "09121234567",
    "09123334455",
]

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
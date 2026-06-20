from django.apps import AppConfig

class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    verbose_name = 'پنل دانشجو'

    def ready(self):
        # اگر سیگنال ندارید، این خط رو بذارید
        pass
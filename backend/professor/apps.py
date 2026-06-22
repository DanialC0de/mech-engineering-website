from django.apps import AppConfig

class ProfessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professor'
    verbose_name = 'پنل استاد'

    def ready(self):
        # اگر سیگنال ندارید، این خط رو بذارید
        pass

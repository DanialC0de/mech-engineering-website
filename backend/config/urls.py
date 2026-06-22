from django.contrib import admin
from django.urls import path, include
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('', include('website.urls')),
    path('events/', include('events.urls')),
    path('news/', include('news.urls')),
    path('panel/student/', include('students.urls')),
    path('panel/professor/', include('professor.urls')),
    path('members/', include('members.urls')),
    path('membership/', views.membership_page, name='membership_page'),
]

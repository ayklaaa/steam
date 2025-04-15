from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('www.urls')),  # Главная страница
    path('', include('auth.urls')),  # Например, /login/, /register/
    path('', include('user_profile.urls')),  # Например, /settings/
    path('', include('admin_panel.urls')),  # Например, /dashboard/
]

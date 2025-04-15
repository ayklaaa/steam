from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include('admin_panel.urls')),  # Путь к админ панели вашего приложения
    path('profile/', include('user_profile.urls')),  # Путь к профилю пользователя
    path('', include('auth.urls')),  # Путь к аутентификации
    path('', include('www.urls')),  # Главная страница (если у вас есть приложение www)
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-panel/', include('admin_panel.urls')),  # Путь для административной панели
    path('profile/', include('user_profile.urls')),     # Путь для профиля пользователя
    path('auth/', include('auth.urls')),                 # Путь для аутентификации
    path('', include('www.urls')),                       # Главная страница (можно оставить пустым, но не дублировать)
]

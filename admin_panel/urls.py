from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),  # Главная панель
    path('admin/users/', views.admin_users, name='admin_users'),  # Страница пользователей
    path('admin/games/', views.admin_games, name='admin_games'),  # Страница игр
    path('admin/category/', CategoryView.as_view(), name='category'),  # Страница категорий
    path('admin/comments/', views.admin_comments, name='admin_comments'),  # Страница комментариев
    path('admin/ratings/', views.admin_ratings, name='admin_ratings'),  # Страница рейтингов
    path('admin/favorites/', views.admin_favorites, name='admin_favorites'),  # Страница избранных игр
    path('admin/stats/', views.admin_stats, name='admin_stats'),  # Страница статистики
    path('admin/status/', StatusView.as_view(), name='admin_status'),  # Страница статистики

    path('add_tag/', views.add_tag, name='add_tag'),
    path('edit_tag/<int:id>/', views.edit_tag, name='edit_tag'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_status/', views.add_status, name='add_status'),
    path('add_teglist/', views.add_teglist, name='add_teglist'),
    path('delete_tag/<int:pk>/', deleteteg.as_view(), name='delete_tag'),
    path('delete_com/<int:pk>/', deletecom.as_view(), name='delete_com'),
    path('edit-game/<int:pk>/', EditGameView.as_view(), name='edit_game'),
]

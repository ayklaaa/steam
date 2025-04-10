from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin-panel/', include('admin_panel.urls')),
    path('', include('www.urls')),
    path('', include('user_profile.urls')),
    path('', include('auth.urls')),
    path('', include('admin_panel.urls')),
]

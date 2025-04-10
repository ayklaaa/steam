from functools import partial

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='update'),
    path('profile/<int:pk>/follower/', FollowerView.as_view(), name='follower'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/friend/', toggle_friend, name='toggle-friend'),
    path('profile/<int:pk>/follower/', FollowersDeleteView.as_view(), name='delete-friend'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

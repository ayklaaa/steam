from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *
from .views import login_view
app_name = 'auth'
handler404 = NotFound

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterCreateView.as_view(), name='reg'),

]

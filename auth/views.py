from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse_lazy
from django.views.generic import CreateView


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'auth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect('index')

    context = {
        'message': 'НЕПРАВИЛЬНО',
    }
    return render(request, 'auth/login.html', context)


def logout_view(request):
    auth.logout(request)
    return redirect('auth:login')


class RegisterCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)  # Сначала сохранить пользователя
        login(self.request, self.object)  # Затем авторизовать его
        return response  # Перенаправление на success_url


def NotFound(request):
    return render(request, 'exception.html', status=404)

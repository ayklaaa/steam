from cProfile import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from user_profile.models import *
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from www.models import MGame

# def ProfileView(request):
#     return render(request,'profile/profile.html')

# class ProfileListView(ListView):
#     model = MUserProfile
#     template_name = 'profile/profile.html'
#     context_object_name = 'profiles'
#
#
# def list_games(request):
#     user_profile = MUserProfile.objects.filter(user=request.user).first()  # Получаем профиль пользователя
#
#     if user_profile:
#         games = user_profile.game.all()  # Все игры пользователя
#     else:
#         games = []  # Если профиля нет, передаём пустой список
#
#     print(f"User: {request.user}, Games: {[game.name for game in games]}")  # Проверяем в консоли
#
#     return render(request, 'profile/profile.html', {'games': games})  # Передаём `games` в шаблон
#
#
# class ProfileListView(LoginRequiredMixin, ListView):
#     model = MUserProfile
#     template_name = 'profile/profile.html'
#     context_object_name = 'profiles'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = MUserProfile.objects.filter(user=self.request.user).first()
#         context['games'] = user_profile.game.all() if user_profile else []
#         return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = MUserProfile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile_pk = self.kwargs.get("pk")  # Получаем pk из URL
        if profile_pk:
            return MUserProfile.objects.get(pk=profile_pk)  # Загружаем профиль по ID
        return MUserProfile.objects.get(user=self.request.user)  # Если pk нет, загружаем свой профиль

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # Игры, добавленные пользователем
        my_games = MGame.objects.filter(creator=profile)

        tegs = Teg.objects.filter(user=profile.user).exclude(game__in=my_games)

        context['tegs'] = tegs
        context['my_games'] = my_games

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MUserProfile
    template_name = 'update.html'
    success_url = reverse_lazy('profile')  # URL страницы профиля
    context_object_name = 'profile'
    fields = ['profile_picture', 'name', 'description', 'birth_date']

    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        self.is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        profile = super().get_object(queryset)
        if profile.user != self.request.user:
            raise HttpResponseForbidden("You can't edit someone else's profile!")
        return profile

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        if self.is_ajax:
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('profile'),  # URL для перенаправления
                'profile_picture_url': self._get_profile_picture_url(),
                'name': self.object.name,
                'description': self.object.description,
                'birth_date': self._get_formatted_birth_date()
            })
        return response

    def form_invalid(self, form):
        if self.is_ajax:
            return JsonResponse({
                'success': False,
                'errors': {field: errors[0] for field, errors in form.errors.items()}
            }, status=400)
        return super().form_invalid(form)

    def _get_profile_picture_url(self):
        if self.object.profile_picture and hasattr(self.object.profile_picture, 'url'):
            return self.object.profile_picture.url
        return '/static/img/ava.png'

    def _get_formatted_birth_date(self):
        return self.object.birth_date.strftime('%Y-%m-%d') if self.object.birth_date else None
class FollowerView(LoginRequiredMixin, ListView):
    model = MUserProfile
    template_name = 'profile/follower.html'
    context_object_name = 'friends'

    def get_queryset(self):
        user_profile = get_object_or_404(MUserProfile, pk=self.kwargs['pk'])
        return user_profile.friends.all()

class FollowersDeleteView(LoginRequiredMixin, DeleteView):
    model = MUserProfile
    template_name = 'profile/follower.html'
    context_object_name = 'friends'
    success_url = reverse_lazy('profile')


@login_required
def toggle_friend(request, pk):
    profile = get_object_or_404(MUserProfile, pk=pk)
    user_profile = request.user.muserprofile

    if profile in user_profile.friends.all():
        user_profile.friends.remove(profile)
        profile.friends.remove(user_profile)
    else:
        user_profile.friends.add(profile)
        profile.friends.add(user_profile)

    return redirect(reverse('profile-detail', kwargs={'pk': pk}))



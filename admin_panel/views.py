
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView

from user_profile.models import *
from www.forms import ImageFormSet, GameForm
from www.models import *
from .forms import MStatusForm, MTeglistForm
from .models import *
from django.db.models import Count

# Представление для главной панели админа
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    return render(request, 'admin_panel/dashboard.html')

# Страница управления пользователями

@login_required
def admin_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = MUserProfile.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})
# Страница управления играми
@login_required
def admin_games(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    games = MGame.objects.all()
    return render(request, 'admin_panel/games.html', {'games': games})

# Страница управления тегами
def admin_tags(request):
    tags = TegList.objects.all()
    return render(request, 'admin_panel/tags.html', {'tags': tags})

@login_required
def admin_comments(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    comments = MComment.objects.all()
    return render(request, 'admin_panel/comments.html', {'comments': comments})

# Страница управления рейтингами
def admin_ratings(request):
    ratings = MRating.objects.all()
    return render(request, 'admin_panel/ratings.html', {'ratings': ratings})

# Страница избранных игр
def admin_favorites(request):
    favorites = MFavoriteGame.objects.all()
    return render(request, 'admin_panel/favorites.html', {'favorites': favorites})

# Страница статистики
def admin_stats(request):
    total_users = MUserProfile.objects.count()
    total_games = MGame.objects.count()
    total_comments = MComment.objects.count()
    total_ratings = MRating.objects.count()

    return render(request, 'admin_panel/stats.html', {
        'total_users': total_users,
        'total_games': total_games,
        'total_comments': total_comments,
        'total_ratings': total_ratings,
    })




@login_required
def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        # Создаем новый тег
        new_tag = TegList.objects.create(name=name)

        return HttpResponse("Tag added successfully!")

    return render(request, 'admin_panel/add_tag.html')

@login_required
def edit_tag(request, id):
    tag = get_object_or_404(TegList, id=id)

    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.save()
        return redirect('admin_tags')  # Перенаправление на страницу со списком тегов

    return render(request, 'admin_panel/edit_tag.html', {'tag': tag})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            MCategory.objects.create(name=name)  # Создание новой категории
            return redirect('add_category')  # Перенаправление на страницу со списком категорий

    return render(request, 'admin_panel/add_category.html')

def add_status(request):
    if request.method == 'POST':
        form = MStatusForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новый статус в базе данных
            return redirect('admin_dashboard')  # Перенаправляем на список статусов
    else:
        form = MStatusForm()  # Создаем пустую форму

    return render(request, 'admin_panel/add_status.html', {'form': form})

def add_teglist(request):
    if request.method == 'POST':
        form = MTeglistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # потом сюда страницу списка тегов
    else:
        form = MTeglistForm()

    return render(request, 'admin_panel/add_teglist.html', {'form': form})

class deleteteg(DeleteView):
    model = MGame
    template_name = 'admin_panel/delete.html'
    success_url = '/admin/games/'

class deletecom(DeleteView):
    model = MComment
    template_name = 'admin_panel/delete.html'
    success_url = '/admin/comments/'
class CategoryView(ListView):
    model = MCategory
    template_name = 'admin_panel/category.html'
    context_object_name = 'category'

class StatusView(ListView):
    model = MStatus
    template_name = 'admin_panel/status.html'
    context_object_name = 'status'


class GameEditView(LoginRequiredMixin, UpdateView):
    model = MGame
    context_object_name = 'game'
    template_name = 'admin_panel/edit_game.html'
    form_class = GameForm
    success_url = '/admin/games/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        self.object = form.save()

        if image_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()
        else:
            self.object.delete()
            return self.form_invalid(form)

        return super().form_valid(form)

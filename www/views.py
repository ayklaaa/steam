from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from user_profile.models import *
from .forms import *
from .models import *
from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from www.models import MGame
from .models import MUserProfile
from .forms import GameForm, ImageFormSet


# def game_list(request):
#     games = MGame.objects.all().order_by('-id')
#     paginator = Paginator(games, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#
#         html = ""
#         for game in page_obj:
#             html += f"""
#                    <div class="game-block" data-game="{game.id}">
#                        {'<img src="' + game.image.url + '" class="game-cover">' if game.image else '<div class="no-image">No cover</div>'}
#                        <div class="title-game">
#                            <div class="name">
#                                <h3 class="game-title">{game.name}</h3>
#                                <p class="game-description">{game.description}</p>
#                            </div>
#                            <div class="info-button">Category</div>
#                        </div>
#                        <div class="modal">
#                            <!-- ... ваш модальный контент ... -->
#                        </div>
#                    </div>
#                    """
#         return JsonResponse({'html': html, 'has_next': page_obj.has_next()})
#
#     return render(request, 'index.html', {'games': page_obj.object_list[:6]})
# def index(request):
#     games = MGame.objects.all()
#     context = {
#         'games': games,
#     }
#     return render(request, 'index.html', context=context)


class IndexView(ListView):
    model = MGame
    template_name = 'index.html'
    context_object_name = 'games'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = MUserProfile.objects.filter(user=self.request.user).first()
            context['user_profile'] = profile
            if profile:
                context['friends'] = profile.friends.all()
            else:
                context['friends'] = []
        else:
            context['user_profile'] = None
            context['friends'] = []

        context['high_rated_games'] = MGame.objects.filter(average_rating__gt=4.5)
        return context


# def game_detail(request, game_id):
#     game = MGame.objects.get(id=game_id)
#     categories = game.category.all()  # Получаем связанные категории
#
#     return render(request, 'index.html', {
#         'game': game,
#         'categories': categories
#     })


class GameDetailView(DetailView):
    model = MGame
    template_name = 'detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object  # Текущая игра

        # Разбиваем about на заголовки и описания
        lines = game.about.split("\n")
        features = []

        for line in lines:
            if line.startswith("* "):  # Заголовок
                features.append({"title": line[2:], "description": ""})
            elif features and line.strip():  # Описание к последнему заголовку
                features[-1]["description"] += line + " "

        # Добавляем данные о рейтинге
        context["features"] = features
        context["average_rating"] = game.get_average_rating()
        context["rating_count"] = game.get_rating_count()

        # Проверяем, поставил ли текущий пользователь оценку
        if self.request.user.is_authenticated:
            user_profile = self.request.user.muserprofile  # Предполагается OneToOne связь
            try:
                user_rating = MRating.objects.get(user=user_profile, game=game)
                context["user_rating"] = user_rating.rating
            except MRating.DoesNotExist:
                context["user_rating"] = None
        else:
            context["user_rating"] = None

        # Добавляем комментарии
        context["comments"] = game.comments.all().order_by("-date_posted")  # Загружаем все комментарии
        context["comment_form"] = CommentForm()  # Форма для добавления комментариев
        context["tags"] = TegList.objects.all()  # Получаем все теги
        context["tag_form"] = TagSelectionForm()  # Форма для тегов

        # Получаем статусы "Playing now" и "Played"
        playing_now_status = get_object_or_404(TegList, name="Playing now")
        played_status = get_object_or_404(TegList, name="Played")

        # Считаем количество уникальных пользователей
        context["playing_now"] = Teg.objects.filter(game=game, status=playing_now_status).values("user").distinct().count()
        context["played"] = Teg.objects.filter(game=game, status=played_status).values("user").distinct().count()
        context["favorite"] = MFavoriteGame.objects.filter(game=game).values("user").distinct().count()

        return context


@login_required
def add_comment(request, game_id):
    """Добавление комментария к игре"""
    game = get_object_or_404(MGame, id=game_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.game = game
            comment.save()

    return redirect("detail", pk=game.id)


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(MComment, id=comment_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect('detail', pk=comment.game.id)  # Перенаправление на ту же страницу

    return redirect('detail', pk=comment.game.id)


@login_required
def like_comment(request, comment_id):
    """Лайк или дизлайк комментария (переключение)"""
    comment = get_object_or_404(MComment, id=comment_id)
    user = request.user

    # Проверяем, существует ли уже реакция
    reaction, created = MCommentReaction.objects.get_or_create(
        user=user, comment=comment, defaults={"reaction": MCommentReaction.LIKE}
    )

    if not created:
        if reaction.reaction == MCommentReaction.LIKE:
            reaction.delete()  # Если уже лайк, убираем его
        else:
            reaction.reaction = MCommentReaction.LIKE
            reaction.save()

    return JsonResponse({"likes": comment.like_count(), "dislikes": comment.dislike_count()})


@login_required
def dislike_comment(request, comment_id):
    """Дизлайк комментария (переключение)"""
    comment = get_object_or_404(MComment, id=comment_id)
    user = request.user

    # Проверяем, существует ли уже реакция
    reaction, created = MCommentReaction.objects.get_or_create(
        user=user, comment=comment, defaults={"reaction": MCommentReaction.DISLIKE}
    )

    if not created:
        if reaction.reaction == MCommentReaction.DISLIKE:
            reaction.delete()  # Если уже дизлайк, убираем его
        else:
            reaction.reaction = MCommentReaction.DISLIKE
            reaction.save()

    return JsonResponse({"likes": comment.like_count(), "dislikes": comment.dislike_count()})


@login_required
def like_reply(request, reply_id):
    """Лайк или дизлайк ответа (переключение)"""
    reply = get_object_or_404(MReply, id=reply_id)
    user = request.user

    reaction, created = MReplyReaction.objects.get_or_create(
        user=user, reply=reply, defaults={"reaction": MCommentReaction.LIKE}
    )

    if not created:
        if reaction.reaction == MCommentReaction.LIKE:
            reaction.delete()  # Если уже лайк, убираем его
        else:
            reaction.reaction = MCommentReaction.LIKE
            reaction.save()

    return JsonResponse({"likes": reply.like_count(), "dislikes": reply.dislike_count()})


@login_required
def dislike_reply(request, reply_id):
    """Дизлайк ответа (переключение)"""
    reply = get_object_or_404(MReply, id=reply_id)
    user = request.user

    reaction, created = MReplyReaction.objects.get_or_create(
        user=user, reply=reply, defaults={"reaction": MCommentReaction.DISLIKE}
    )

    if not created:
        if reaction.reaction == MCommentReaction.DISLIKE:
            reaction.delete()  # Если уже дизлайк, убираем его
        else:
            reaction.reaction = MCommentReaction.DISLIKE
            reaction.save()

    return JsonResponse({"likes": reply.like_count(), "dislikes": reply.dislike_count()})


@login_required
def rate_game(request, game_id):
    game = get_object_or_404(MGame, id=game_id)
    user_profile = request.user.muserprofile  # Проверяем профиль пользователя

    if request.method == "POST":
        rating_value = int(request.POST.get("rating", 0))
        if 1 <= rating_value <= 5:
            # Обновляем или создаем рейтинг
            rating, created = MRating.objects.update_or_create(
                user=user_profile, game=game,
                defaults={"rating": rating_value}
            )

    return redirect("detail", pk=game.id)  # Перенаправляем обратно


class CatalogView(ListView):
    model = MGame
    template_name = 'catalog.html'
    context_object_name = 'games'
    paginate_by = 18

    def get_queryset(self):
        queryset = MGame.objects.all()
        category_id = self.kwargs.get('category_id')  # Теперь получаем из URL, а не GET
        if category_id:
            queryset = queryset.filter(category__id=category_id)  # Правильная фильтрация
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id:
            context['selected_category'] = get_object_or_404(MCategory, id=category_id)
        return context


class AutorsView(ListView):
    model = MGame
    template_name = 'autors.html'
    context_object_name = 'games'


# Create your views here.

class WishlistView(ListView):
    model = MGame
    template_name = 'wishlist.html'
    context_object_name = 'games'
    paginate_by = 18


# class AddGameView(CreateView):
#     model = MGame
#     template_name = 'addgame.html'
#     context_object_name = 'game'
#     form_class = GameForm
#
#     def form_valid(self, form):
#         # Устанавливаем текущего пользователя как создателя игры
#         form.instance.creator = MUserProfile.objects.get(user=self.request.user)
#         return super().form_valid(form)
class AddGameView(LoginRequiredMixin, CreateView):
    model = MGame
    template_name = 'addgame.html'
    form_class = GameForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        form.instance.creator = MUserProfile.objects.get(user=self.request.user)
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


class AddTagToGameView(View):
    def post(self, request, game_id):
        game = get_object_or_404(MGame, id=game_id)
        tag_id = request.POST.get('status')
        if request.user.is_authenticated:
            user = request.user
            status = get_object_or_404(TegList, id=tag_id)

            # Если запись уже существует, обновляем тег, иначе создаем новую запись
            teg, created = Teg.objects.update_or_create(
                user=user,
                game=game,
                defaults={'status': status}
            )

        return redirect('detail', pk=game.id)  # или 'game_detail', в зависимости от имени URL


@login_required
def add_to_wishlist(request):
    if request.method == "POST":
        game_id = request.POST.get("game_id")
        game = get_object_or_404(MGame, id=game_id)
        user_profile = MUserProfile.objects.get(user=request.user)

        # Проверяем, не добавлена ли уже игра в избранное
        favorite, created = MFavoriteGame.objects.get_or_create(user=user_profile, game=game)

        return JsonResponse({"status": "added" if created else "exists"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def load_more_games(request):
    offset = int(request.GET.get("offset", 0))
    limit = 6
    games = MGame.objects.all()[offset:offset + limit]

    data = {
        "games": [
            {
                "id": game.id,
                "name": game.name,
                "description": game.description,
                "image": game.image.url if game.image else None,
                "categories": [{"id": category.id, "name": category.name} for category in game.category.all()]

            }
            for game in games
        ],
        "has_more": MGame.objects.count() > offset + limit  # Проверяем, есть ли еще игры
    }

    return JsonResponse(data)


@login_required
def wishlist_view(request):
    user_profile = request.user.muserprofile  # Получаем профиль пользователя
    wishlist_games = MFavoriteGame.objects.filter(user=user_profile).select_related('game')

    return render(request, "wishlist.html", {"wishlist_games": wishlist_games})


def search_items(model, field, search):
    """Функция для поиска объектов модели по полю."""
    filter_params = {f"{field}__icontains": search}
    return model.objects.filter(**filter_params)


@login_required()
def search(request):
    context = {'error': 'Вы не ввели ничего для поиска'}

    if request.method == 'GET':
        search_query = request.GET.get('search', '').strip()
        if search_query:
            context = {
                'search': search_query,
                'games': search_items(MGame, 'name', search_query),
                'profiles': search_items(MUserProfile, 'name', search_query),
                'categories': search_items(MCategory, 'name', search_query),
                'statuses': search_items(MStatus, 'name', search_query),
            }

    return render(request, 'search.html', context=context)



from functools import partial

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/category/<int:category_id>/', CatalogView.as_view(), name='game_catalog_by_category'),

    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('autors', AutorsView.as_view(), name='autors'),
    path('wishlist', wishlist_view, name='wishlist'),
    # path('', game_detail, name='index'),
    path("game/<int:game_id>/rate/", rate_game, name="rate_game"),
    path('game/<int:pk>', GameDetailView.as_view(), name='detail'),

    path("game/<int:game_id>/comment/", add_comment, name="add_comment"),
    path('comment/<int:comment_id>/reply/', add_reply, name='add_reply'),
    path("comment/<int:comment_id>/like/", like_comment, name="like_comment"),
    path("comment/<int:comment_id>/dislike/", dislike_comment, name="dislike_comment"),

    # path("upload-images/", upload_images, name="upload_images"),
    path('search/', search, name='search'),

    path('add/', AddGameView.as_view(), name='add_game'),
    path("load-more-games/", load_more_games, name="load-more-games"),
    path('game/<int:game_id>/add_tag/', AddTagToGameView.as_view(), name='add_tag_to_game'),
    path("add_to_wishlist/", add_to_wishlist, name="add_to_wishlist"),
    path("comment/<int:comment_id>/like/", like_comment, name="like_comment"),
    path("comment/<int:comment_id>/dislike/", dislike_comment, name="dislike_comment"),
    path('reply/<int:reply_id>/like/', like_reply, name='like_reply'),
    path('reply/<int:reply_id>/dislike/', dislike_reply, name='dislike_reply'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

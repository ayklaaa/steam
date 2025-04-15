from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from www.models import *

class MUserProfile(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField(
        'image',
        folder='profile_pictures',
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)
    game = models.ManyToManyField('www.MGame', blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    friends = models.ManyToManyField('MUserProfile', blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'



    def add_to_favorites(self, game):
        """Добавляет игру в избранное пользователя."""
        MFavoriteGame.objects.get_or_create(user=self, game=game)

    def remove_from_favorites(self, game):
        """Удаляет игру из избранного пользователя."""
        MFavoriteGame.objects.filter(user=self, game=game).delete()

    def get_favorite_games(self):
        """Возвращает список избранных игр пользователя."""
        return [fav.game for fav in self.favorite_games.all()]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MUserProfile.objects.get_or_create(user=instance, defaults={'name': instance.username})

class TegList(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self):
        return f'{self.name}'

class Teg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('www.MGame', on_delete=models.CASCADE)
    status = models.ForeignKey(TegList, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.game} - {self.status}'

    class Meta:
        unique_together = ('user', 'game')


class MFavoriteGame(models.Model):
    user = models.ForeignKey(MUserProfile, on_delete=models.CASCADE, related_name='favorite_games')
    game = models.ForeignKey('www.MGame', on_delete=models.CASCADE, related_name='favorited_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f'{self.user.name} добавил в избранное {self.game.name}'

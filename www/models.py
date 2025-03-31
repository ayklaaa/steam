from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

from user_profile.models import MUserProfile


class MCategory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class MStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class MGame(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField('MCategory')
    description = models.TextField()
    image = models.ImageField(upload_to='games/', blank=True)
    video = models.FileField(upload_to='games/', blank=True)
    about = models.TextField()
    # rating = models.IntegerField()
    average_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    # comment = models.TextField(blank=True, null=True)
    status = models.ForeignKey(MStatus, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    creator = models.ForeignKey('user_profile.MUserProfile', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        categories = ", ".join([cat.name for cat in self.category.all()])
        return f'{self.name} - {categories}'

    def add_rating(self, user, rating):
        """Добавляет или обновляет оценку пользователя для игры."""
        MRating.objects.update_or_create(
            user=user,
            game=self,
            defaults={'rating': rating}
        )

    def get_average_rating(self):
        """Возвращает средний рейтинг игры."""
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0

    def get_rating_count(self):
        """Возвращает количество оценок игры."""
        return self.ratings.count()

    def update_rating(self):
        """Обновляет средний рейтинг и количество оценок."""
        ratings = self.ratings.all()
        self.rating_count = ratings.count()
        if self.rating_count > 0:
            self.average_rating = sum(r.rating for r in ratings) / self.rating_count
        else:
            self.average_rating = 0
        self.save()


class MImage(models.Model):
    game = models.ForeignKey(MGame, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'Image for game: {self.game.name}'
class MComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(MGame, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.game.name}'

    def like_count(self):
        return self.reactions.filter(reaction=MCommentReaction.LIKE).count()

    def dislike_count(self):
        return self.reactions.filter(reaction=MCommentReaction.DISLIKE).count()

class MReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(MComment, on_delete=models.CASCADE, related_name="replies")
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ответ от {self.user.username} на комментарий {self.comment.id}'

    def like_count(self):
        return self.reactions.filter(reaction=MCommentReaction.LIKE).count()

    def dislike_count(self):
        return self.reactions.filter(reaction=MCommentReaction.DISLIKE).count()


class MCommentReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(MComment, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    date_reacted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user.username} - {self.reaction} на комментарий {self.comment.id}'



class MReplyReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey("MReply", on_delete=models.CASCADE, related_name="reactions")  # Ответ, на который ставится реакция
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("user", "reply")

    def __str__(self):
        return f"{self.user.username} - {self.reaction} на ответ {self.reply.id}"



class MRating(models.Model):
    user = models.ForeignKey(MUserProfile, on_delete=models.CASCADE, related_name='ratings')
    game = models.ForeignKey(MGame, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f'{self.user.name} оценил {self.game.name} на {self.rating}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.game.update_rating()


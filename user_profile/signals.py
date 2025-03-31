from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MUserProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not MUserProfile.objects.filter(user=instance).exists():
        MUserProfile.objects.create(user=instance, name=instance.username)

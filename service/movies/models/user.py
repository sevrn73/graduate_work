from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    external_access_token = models.CharField("external_access_token", default="", max_length=1500)
    external_refresh_token = models.CharField("external_refresh_token", default="", max_length=1500)
    chosen_room_id = models.UUIDField(default=None, null=True)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

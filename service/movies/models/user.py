from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    external_access_token = models.CharField("external_jwt_token", default="", max_length=120)
    external_refresh_token = models.CharField("external_jwt_token", default="", max_length=120)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)

    class Meta:
        abstract = True


class Room(UUIDMixin, TimeStampedMixin):
    owner_uuid = models.UUIDField(default=uuid.uuid4, null=False, unique=True)
    film_work_uuid = models.UUIDField(default=uuid.uuid4, null=True)
    film_work_time = models.FloatField(_("name"), null=True)
    film_work_state = models.CharField(_("name"), max_length=255, null=True)

    class Meta:
        db_table = "cinema_together_room"
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return f"{self.owner_uuid}-{self.film_work_uuid}"


class RoomUser(UUIDMixin, TimeStampedMixin):
    user_uuid = models.UUIDField(default=uuid.uuid4)

    class RoomUserType(models.TextChoices):
        pending = "pending"
        member = "member"
        owner = "owner"

    user_type = models.CharField(
        _("user_type"), choices=RoomUserType.choices, default=RoomUserType.pending, max_length=8
    )
    room = models.ForeignKey("Room", db_column="room_uuid", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "cinema_together_room_user"
        verbose_name = _("RoomUser")
        verbose_name_plural = _("RoomUsers")

    def __str__(self):
        return f"{self.user_uuid}"

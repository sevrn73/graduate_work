import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("owner_uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("film_work_uuid", models.UUIDField(default=uuid.uuid4)),
                ("film_work_time", models.FloatField(verbose_name="name")),
                ("film_work_state", models.CharField(max_length=255, verbose_name="name")),
            ],
            options={
                "verbose_name": "Room",
                "verbose_name_plural": "Rooms",
                "db_table": "cinema_together_room",
            },
        ),
        migrations.CreateModel(
            name="RoomUser",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("user_uuid", models.UUIDField(default=uuid.uuid4)),
                (
                    "user_type",
                    models.CharField(
                        choices=[("pending", "Pending"), ("member", "Member"), ("owner", "Owner")],
                        default="pending",
                        max_length=8,
                        verbose_name="user_type",
                    ),
                ),
                ("room_uuid", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.room")),
            ],
            options={
                "verbose_name": "RoomUser",
                "verbose_name_plural": "RoomUsers",
                "db_table": "cinema_together_room_user",
            },
        ),
    ]

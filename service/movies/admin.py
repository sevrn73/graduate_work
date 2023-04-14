from django.contrib import admin
from movies.models import Profile, Room, RoomUser


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner_uuid",
        "film_work_uuid",
        "film_work_state",
    )
    list_filter = (
        "owner_uuid",
        "film_work_state",
    )


@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_uuid",
        "user_type",
        "room",
    )

    list_filter = ("user_type",)


admin.site.register(Profile)

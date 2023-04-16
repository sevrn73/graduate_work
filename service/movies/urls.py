# yapf: disable
from django.urls import path
from movies.views import change_chosen_room_id, cinema_together, index, login, logout, register

urlpatterns = [
    path('', index, name="index"),
    path('change_chosen_room_id/<str:chosen_room_id>', change_chosen_room_id, name='change_chosen_room_id'),
    path('cinema_together', cinema_together, name="cinema_together"),
    path("logout", logout, name="logout"),
    path("login", login, name="login"),
    path("register", register, name="register"),
]

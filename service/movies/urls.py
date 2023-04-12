# yapf: disable
from django.urls import path
from movies.views import index, login, logout, register

urlpatterns = [
    path('', index, name="index"),
    path("logout", logout, name="logout"),
    path("login", login, name="login"),
    path("register", register, name="register"),
]

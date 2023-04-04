from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.views.generic import View
from movies.models.user import Profile


class Login(View):
    """
    Классы с реализацией формы логирования

    """

    def login(request, username: str, password: str):
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
        else:
            return {"err": "Введен неверный логин или пароль"}

    def logout(request):
        auth.logout(request)
        auth.logout(request)
        return HttpResponseRedirect("/")


class Registration(View):
    """
    Классы с реализацией формы регистрации

    """

    def registr(request, username: str, password: str, team: str):
        if User.objects.filter(username=username).exists():
            return {"err": "Пользователь уже зарегистрирован"}
        else:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.profile.external_access_token = response["access_token"]
            new_user.profile.external_refresh_token = response["refresh_token"]
            new_user.save()

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)

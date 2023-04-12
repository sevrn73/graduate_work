from http import HTTPStatus

import requests
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render


def index(request):
    context = {}
    response = requests.get(
        "http://nginx:80/cinema_v1/room/",
        headers={
            "Authorization": "Bearer "
            + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMiIsImZpcnN0X25hbWUiOiJKb2huIiwibGFzdF9uYW1lIjoiRG9lIn0.nRfn2tSNVmc_E4h1k9rShEOM3Bgxtd1FkVKn3u2k23Y"
        },  # request.user.profile.external_access_token}
    )
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        context["room_id"] = data["id"]
    return render(request, "index.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"err": "Пользователь не зарегистрирован"})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"err": "Пользователь уже зарегистрирован"})
        else:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.profile.external_access_token = "123"
            new_user.profile.external_refresh_token = "123"
            new_user.save()

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
            return render(request, "login.html", {"err": "Пользователь успешно зарегистрирован"})
    else:
        return render(request, "register.html")


def logout(request):
    auth.logout(request)
    auth.logout(request)
    return HttpResponseRedirect("/login")

from base64 import b64encode
from http import HTTPStatus

import backoff
import requests
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from example.settings import LOGIN_JWT_URL, LOGOUT_JWT_URL, SIGNUP_JWT_URL
from movies.models.movies import Film


def index(request):
    return render(
        request,
        "index.html",
        {"film_works_data": list(Film.objects.all().values("id", "film_work_name", "film_work_url_id"))},
    )


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_time=120,
)
def get_room_data(room_id, external_access_token):
    response = requests.get(
        f"http://nginx:80/cinema_v1/room/{room_id}",
        headers={"Authorization": "Bearer " + external_access_token},
    )
    if response.status_code not in [HTTPStatus.OK, HTTPStatus.FORBIDDEN]:
        raise requests.exceptions.RequestException
    else:
        return response


def cinema_together(request):
    room_id = request.user.profile.chosen_room_id
    response = get_room_data(room_id, request.user.profile.external_access_token)

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        return render(
            request,
            "cinema_together.html",
            {
                "room_id": room_id,
                "owner_id": data["owner_uuid"],
                "film_work_url": Film.objects.filter(id=data["film_work_uuid"])
                .values("film_work_url_id")
                .first()["film_work_url_id"],
            },
        )
    elif response.status_code == HTTPStatus.FORBIDDEN:
        return HttpResponseRedirect("/")


def change_chosen_room_id(request, chosen_room_id: str):
    request.user.profile.chosen_room_id = chosen_room_id
    request.user.profile.save()
    return HttpResponse(status=HTTPStatus.OK)


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        response = requests.post(
            LOGIN_JWT_URL,
            headers={"Authorization": basic_auth(username, password)},
        )
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            user_model = User.objects.filter(username=username).first()
            user_model.profile.external_access_token = data["access_token"]
            user_model.profile.external_refresh_token = data["refresh_token"]
            user_model.profile.save()

            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"err": "Пользователь не зарегистрирован"})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"err": "Пользователь уже зарегистрирован"})
        else:
            response = requests.post(
                SIGNUP_JWT_URL,
                data={
                    "login": username,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            if response.status_code == HTTPStatus.OK:
                data = response.json()
                new_user = User.objects.create_user(username=username, password=password)
                new_user.profile.external_access_token = data["access_token"]
                new_user.profile.external_refresh_token = data["refresh_token"]
                new_user.profile.save()

                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return HttpResponseRedirect("/login")
            else:
                return render(request, "register.html", {"err": "Пользователь с такими данными уже зарегистрирован"})
    else:
        return render(request, "register.html")


def logout(request):
    requests.delete(
        LOGOUT_JWT_URL,
        headers={"Authorization": "Bearer " + request.user.profile.external_access_token},
    )
    auth.logout(request)
    return HttpResponseRedirect("/login")

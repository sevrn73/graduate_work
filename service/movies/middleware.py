from http import HTTPStatus

import requests
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from example.settings import LOGOUT_JWT_URL, REFRESH_JWT_URL, VERIFY_JWT_URL


class ProcessRequestMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        path = request.path_info.lstrip("/")
        if not any([path.startswith(_) for _ in ["admin/", "login", "logout", "register", "change_chosen_room_id"]]):
            user = request.user
            if user.is_authenticated:
                response = requests.get(
                    VERIFY_JWT_URL,
                    headers={"Authorization": "Bearer " + request.user.profile.external_access_token},
                )
                if response.status_code == HTTPStatus.OK:
                    return
                else:
                    # пробуем получить новый access token
                    response = requests.get(
                        REFRESH_JWT_URL,
                        headers={"Authorization": "Bearer " + request.user.profile.external_refresh_token},
                    )
                    if response.status_code == HTTPStatus.OK:
                        data = response.json()
                        user.profile.external_access_token = data["access_token"]
                        user.profile.external_refresh_token = data["refresh_token"]
                        user.profile.save()
                        return
                    else:
                        requests.delete(
                            LOGOUT_JWT_URL,
                            headers={"Authorization": "Bearer " + request.user.profile.external_access_token},
                        )
                        auth.logout(request)
                        auth.logout(request)
                        return HttpResponseRedirect("/login")
            else:
                return HttpResponseRedirect("/login")

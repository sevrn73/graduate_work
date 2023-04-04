from http import HTTPStatus

import httpx
from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from example.settings import REFRESH_JWT_URL, VERIFY_JWT_URL


class ProcessRequestMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        path = request.path_info.lstrip("/")
        for endpoint in ["admin/"]:
            if path.startswith(endpoint):
                return

        user = request.user
        if user.is_authenticated:
            with httpx.AsyncClient() as client:
                response = client.get(
                    VERIFY_JWT_URL, headers={"Authorization": "Bearer " + user.profile.external_access_token}
                )
            if response.status_code == HTTPStatus.OK:
                return
            else:
                # пробуем получить новый access token
                with httpx.AsyncClient() as client:
                    response = client.get(
                        REFRESH_JWT_URL,
                        headers={"Authorization": "Bearer " + user.profile.external_refresh_token},
                    )
                if response.status_code == HTTPStatus.OK:
                    user.profile.external_access_token = response["access_token"]
                    user.profile.external_refresh_token = response["refresh_token"]
                    user.profile.save()
                    return
                else:
                    # разлогиниваем пользователя и редирект
                    return HttpResponseRedirect("/login")
        else:
            return HttpResponseRedirect("/login")

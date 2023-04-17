import logging
from http import HTTPStatus

import backoff
import requests
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from example.settings import LOGOUT_JWT_URL, REFRESH_JWT_URL, VERIFY_JWT_URL

logger = logging.getLogger("middleware")


def backoff_handler(details):
    logger.info("Auth is unavailable - sleeping")


class ProcessRequestMiddleware(MiddlewareMixin):
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        on_backoff=backoff_handler,
        max_time=120,
    )
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
                    logger.info(f"verify_jwt smt wrong: {response}")
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
                        logger.info(f"refresh_jwt smt wrong: {response}")
                        requests.delete(
                            LOGOUT_JWT_URL,
                            headers={"Authorization": "Bearer " + request.user.profile.external_access_token},
                        )
                        auth.logout(request)
                        return HttpResponseRedirect("/login")
            else:
                return HttpResponseRedirect("/login")

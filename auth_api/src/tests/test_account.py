import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from src.conftest import TEST_LOGIN, TEST_PASSWORD, access_headers_func

load_dotenv()


def test_sign_up(user):
    response = user
    assert response.status_code == HTTPStatus.OK


def test_login():
    """
    Тестирование авторизации
    """
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        auth=HTTPBasicAuth(TEST_LOGIN, TEST_PASSWORD),
    )
    assert response.status_code == HTTPStatus.OK


def test_login_no_valid_user():
    """
    Тестирование авторизации c неверным паролем
    """
    password_not_vatid = "afafqfqfq"
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        auth=HTTPBasicAuth(TEST_LOGIN, password_not_vatid),
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_history(access_headers):
    """
    Тестирование истории входов
    """
    response = requests.get(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login_history',
        headers=access_headers,
        data={"page": 1, "per_page": 10},
    )
    assert response.status_code == HTTPStatus.OK


def test_logout(access_headers):
    """
    Тестирование Logout
    """
    response = requests.delete(f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/logout', headers=access_headers)
    assert response.status_code == HTTPStatus.OK


def test_refresh(refresh_headers):
    """
    Тестирование refresh
    """
    response = requests.get(f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/refresh', headers=refresh_headers)
    assert response.status_code == HTTPStatus.OK


def test_sing_up():
    """
    Тестирование регистрации
    """
    login = "test_signup"
    password = "qwerty"
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up', data={"login": login, "password": password}
    )
    assert response.status_code == HTTPStatus.OK
    response = requests.post(f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up', data={"login": login})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up', data={"password": password}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_change_login(access_headers):
    """
    Тестирование изменения логина
    """
    new_login = "changed_login"
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/change_login',
        data={"new_login": new_login},
        headers=access_headers,
    )
    assert response.status_code == HTTPStatus.OK
    new_login = "changed_login"
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/change_login',
        data={"new_login": new_login},
        headers=access_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_change_password():
    """
    Тестирование изменения пароля
    """
    new_password = "changed_password"
    header = access_headers_func("changed_login", TEST_PASSWORD)
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/change_password',
        data={"new_password": new_password},
        headers=header,
    )
    assert response.status_code == HTTPStatus.OK

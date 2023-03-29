import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from src.conftest import MANAGING_LOGIN, MANAGING_ROLE, TEST_PASSWORD

load_dotenv()


def test_assign_role(admin_headers, role):
    """
    Тестирование присвоение роли юзеру
    """
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up',
        data={"login": MANAGING_LOGIN, "password": TEST_PASSWORD},
    )
    login = MANAGING_LOGIN
    new_role = MANAGING_ROLE
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/assign_role',
        data={"login": login, "role": new_role},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/assign_role',
        data={"login": login},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/assign_role',
        data={"role": new_role},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_user_roles(admin_headers, role):
    """
    Тестирование вывода списка ролей юзера
    """
    login = MANAGING_LOGIN
    response = requests.get(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/user_roles',
        data={"login": login},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK


def test_detach_role(admin_headers, role):
    """
    Тестирование лишения юзера роли
    """
    login = MANAGING_LOGIN
    new_role = MANAGING_ROLE
    response = requests.delete(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/detach_role',
        data={"login": login, "role": new_role},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK

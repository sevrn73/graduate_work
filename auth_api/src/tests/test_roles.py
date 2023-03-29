import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from src.conftest import ROLE_NAME, ROLE_NAME_NEW

load_dotenv()


def test_create_role(admin_headers):
    """
    Тестирование создания роли
    """

    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/create_role',
        data={"new_role": ROLE_NAME},
        headers=admin_headers,
    )

    assert response.status_code == HTTPStatus.OK
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/create_role',
        data={"new_role": ROLE_NAME},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/create_role',
        data={"new_role": ""},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_change_role(admin_headers):
    """
    Тестирование изменение роли
    """

    response = requests.put(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/change_role',
        data={"role": ROLE_NAME, "new_name": ROLE_NAME_NEW},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK


def test_roles_list(admin_headers):
    """
    Тестирование вывода списка ролей
    """

    response = requests.get(f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/roles_list', headers=admin_headers)
    assert response.status_code == HTTPStatus.OK


def test_delete_role(admin_headers):
    """
    Тестирование удаления роли
    """
    response = requests.delete(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/delete_role',
        data={"role": ROLE_NAME},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.CONFLICT
    response = requests.delete(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/delete_role',
        data={"role": ROLE_NAME_NEW},
        headers=admin_headers,
    )
    assert response.status_code == HTTPStatus.OK

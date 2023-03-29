import base64
import os
import sys
from os.path import abspath
from os.path import dirname as d

import pytest
import requests
from dotenv import load_dotenv

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

load_dotenv()

TEST_LOGIN = "test_login"
TEST_PASSWORD = "test_password"
TEST_LOGIN_NEW = "test_login1"
TEST_PASSWORD_NEW = "test_password2"

ROLE_NAME = "test_role"
ROLE_NAME_NEW = "test_role_new"

MANAGING_LOGIN = "tt_login"
MANAGING_ROLE = "tt_role"


@pytest.fixture()
def user():
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/sign_up',
        data={"login": TEST_LOGIN, "password": TEST_PASSWORD},
    )
    return response


@pytest.fixture(scope="module")
def role(admin_headers):
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/create_role',
        data={"new_role": MANAGING_ROLE},
        headers=admin_headers,
    )
    return response


@pytest.fixture()
def token_response():
    my_str = ":".join((TEST_LOGIN, TEST_PASSWORD)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        headers={"Authorization": "Basic " + credentials},
    )
    return response


@pytest.fixture()
def access_headers(token_response):
    access_token = token_response.json().get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture(scope="module")
def admin_headers():
    admin_login = os.environ.get("SUPERUSER_LOGIN", "admin")
    admin_pass = os.environ.get("SUPERUSER_PASS", "1234")
    my_str = ":".join((admin_login, admin_pass)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        headers={"Authorization": "Basic " + credentials},
    )
    access_token = response.json().get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture()
def refresh_headers(token_response):
    refresh_token = token_response.json().get("refresh_token")
    headers = {"Authorization": "Bearer " + refresh_token}
    return headers


@pytest.fixture()
def not_access_headers():
    login = "not_user"
    password = "not_password"
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    access_token = credentials
    headers = {"Authorization": "Bearer " + access_token}
    return headers


def token_response_func(login, password):
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    response = requests.post(
        f'{os.environ.get("SERVICE_URL", "http://nginx:80")}/v1/login',
        headers={"Authorization": "Basic " + credentials},
    )
    return response


def access_headers_func(login, password):
    access_token = token_response_func(login, password).json().get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    return headers

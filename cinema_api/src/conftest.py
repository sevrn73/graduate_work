import base64
import sys
from os.path import abspath
from os.path import dirname as d

import pytest
import requests
from dotenv import load_dotenv

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

load_dotenv()

TEST_LOGIN = "test_login6"
TEST_PASSWORD = "test_password"
TEST_LOGIN_NEW = "test_login12"
TEST_PASSWORD_NEW = "test_password2"


@pytest.fixture()
def user1():
    response = requests.post(
        f"http://localhost/v1/sign_up",
        data={
            "login": TEST_LOGIN,
            "password": TEST_PASSWORD,
        },
    )
    return response


@pytest.fixture()
def user2():
    response = requests.post(
        f"http://localhost/v1/sign_up",
        data={
            "login": TEST_LOGIN_NEW,
            "password": TEST_PASSWORD_NEW,
        },
    )
    return response


@pytest.fixture()
def access_headers(user1):
    access_token = user1.json().get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture()
def refresh_headers(token_response):
    refresh_token = token_response.json().get("refresh_token")
    headers = {"Authorization": "Bearer " + refresh_token}
    return headers


@pytest.fixture()
def not_access_headers():
    login = "not_user2"
    password = "not_password2"
    my_str = ":".join((login, password)).encode("utf-8")
    credentials = base64.b64encode(my_str).decode("utf-8")
    access_token = credentials
    headers = {"Authorization": "Bearer " + access_token}
    return headers

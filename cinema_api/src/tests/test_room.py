import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from src.conftest import TEST_LOGIN, TEST_PASSWORD

load_dotenv()



# localhost
def test_room(access_headers):
    """
    Тестирование авторизации c неверным паролем
    """
    response = requests.post(f'http://localhost/cinema_v1/room?film_work_uuid=b8e8169d-c58d-4d63-81e3-789468881e1c',json={"film_work_uuid":"b8e8169d-c58d-4d63-81e3-789468881e1c"}, headers=access_headers)
    resp = response.json()
    assert resp["success"] == True
    response = requests.get(f'http://localhost/cinema_v1/room', headers=access_headers)
    resp = response.json()
    assert resp["film_work_uuid"] == "b8e8169d-c58d-4d63-81e3-789468881e1c"
    response = requests.get(f'http://localhost/cinema_v1/room/rooms', headers=access_headers)
    resp = response.json()
    assert len(resp) == 1
    assert resp[0]["film_work_uuid"] == "b8e8169d-c58d-4d63-81e3-789468881e1c"
    room_id = resp[0]["id"]
    response = requests.post(f'http://localhost/cinema_v1/room/{room_id}/delete', headers=access_headers)
    response = requests.get(f'http://localhost/cinema_v1/room', headers=access_headers)
    resp = response.json()
    assert resp["detail"] == "User room not found!"
    response = requests.post(f'http://localhost/cinema_v1/room/{room_id}/delete', headers=access_headers)
    resp = response.json()
    assert resp["success"] == False
    assert resp["errors"] == [f'Room "{room_id}" does not exist!']
    response = requests.get(f'http://localhost/cinema_v1/room', headers=access_headers)
    resp = response.json()
    assert resp["detail"] == "User room not found!"


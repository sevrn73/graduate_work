import requests
from dotenv import load_dotenv

load_dotenv()


# localhost
def test_room(access_headers):
    """
    Тестирование авторизации c неверным паролем
    """
    response = requests.post(
        f"http://localhost/cinema_v1/room/b8e8169d-c58d-4d63-81e3-789468881e1c",
        headers=access_headers,
    )
    resp = response.json()
    assert resp["success"] == True
    response = requests.get(f"http://localhost/cinema_v1/room/", headers=access_headers)
    resp = response.json()
    assert resp["film_work_uuid"] == "b8e8169d-c58d-4d63-81e3-789468881e1c"
    response = requests.get(f"http://localhost/cinema_v1/room/rooms", headers=access_headers)
    resp = response.json()
    assert len(resp) == 1
    assert resp[0]["film_work_uuid"] == "b8e8169d-c58d-4d63-81e3-789468881e1c"
    response = requests.delete(f"http://localhost/cinema_v1/room/delete", headers=access_headers)
    response = requests.get(f"http://localhost/cinema_v1/room/", headers=access_headers)
    resp = response.json()
    assert resp["detail"] == "User room not found!"
    response = requests.delete(f"http://localhost/cinema_v1/room/delete", headers=access_headers)
    resp = response.json()
    assert resp["success"] == False
    assert resp["errors"] == ["Room does not exist!"]
    response = requests.get(f"http://localhost/cinema_v1/room/", headers=access_headers)
    resp = response.json()
    assert resp["detail"] == "User room not found!"

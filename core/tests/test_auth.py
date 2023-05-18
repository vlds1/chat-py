import pytest
from test_data import login_test_data
from test_data import register_test_data


@pytest.mark.parametrize("email, password, expected_res", register_test_data)
def test_registration(client, email, password, expected_res):
    res = client.post(
        "/api/v1/auth/registration", json={"email": email, "password": password}
    )
    assert res.get_json() == expected_res


@pytest.mark.parametrize("email, password, expected_res", login_test_data)
def test_login(client, user_data, email, password, expected_res):
    client.post("/api/v1/auth/registration", json=user_data)
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert expected_res in res.get_json()


def test_refresh_token(client, user_data):
    client.post("/api/v1/auth/registration", json=user_data)
    res = client.post("/api/v1/auth/login", json=user_data)

    refresh_token = res.get_json()["data"]["refresh_token"]
    client.post("/api/v1/auth/token/refresh", json={"refresh_token": refresh_token})
    assert "data" in res.get_json()

def test_registration(user_data, client):
    res = client.post("/api/v1/auth/registration", json=user_data)
    assert res.get_json() == ""

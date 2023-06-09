from starlette import status


def test_get_weather_data(test_client):
    city = "Rostov-on-Don"
    response = test_client.get(f"/api/weather/{city}")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK

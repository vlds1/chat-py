def test_get_weather_data(client):
    city = "Rostov-on-Don"
    response = client.get(f"/api/weather/{city}")
    assert response.status_code == 200

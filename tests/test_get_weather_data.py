from starlette import status


async def test_get_weather_data(mongo_client, async_client):
    city = "Rostov-on-Don"
    response = await async_client.get(f"/api/weather/{city}")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK

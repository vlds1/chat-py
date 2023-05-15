weather_query = """
    query Weather ($city: String){
        CityWeather (city: $city) {
            city
            current_temperature
            current_humidity
            current_weather
            current_wind_speed
            sunrise
            sunset
            day_duration
            request_time
   }
}
    """

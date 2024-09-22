import requests
from datetime import datetime

def get_current_weather_data(api_key):
    """
    Fetches weather data from OpenWeather API for a given city.
    Returns:
    - A dictionary containing relevant weather data or an error message.
    """

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    while True:
        city_name = input("\nEnter a city name: ")

        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Check if the response contains weather data
            if data.get("cod") != 200:
                print(f"Error: {data.get('message', 'Failed to get weather data')}")
                continue  # Prompt the user again for a valid city

            # If the city is valid, return the weather data
            return {
                "city": data.get("name"),
                "temperature": data["main"].get("temp"),
                "max_temperature": data["main"].get("temp_max"),
                "min_temperature": data["main"].get("temp_min"),
                "weather": data["weather"][0].get("description"),
            }

        except requests.RequestException as e:
            print(f"Error: {e}")
            continue  # Retry input in case of request failure


def view_current_weather_data(weather_data):
    print(f"\nThe weather now is: {weather_data.get("weather")} "
          f"The current temperature is {round(weather_data.get('temperature'))}°C.\n\n")



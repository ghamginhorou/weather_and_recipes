from dotenv import load_dotenv
import os

def main():
    load_dotenv()  # Load the variables from .env
    spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY")
    open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")


if __name__ == '__main__':
    main()
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather():
    lat = os.getenv('LAT')
    lon = os.getenv('LON')
    openWeatherAPIKey = os.getenv('OPEN_WEATHER_API_KEY')

    openWeatherURL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openWeatherAPIKey}&units=imperial"

    resp = requests.get(openWeatherURL)
    weather = resp.json()

    return {"weather": {
        "temp": str(round(weather["main"]["temp"])),
        "feels_like": str(round(weather["main"]["feels_like"])),
        "temp_max": str(round(weather["main"]["temp_max"])),
        "temp_min": str(round(weather["main"]["temp_min"])),
        "description": str(weather["weather"][0]["description"])
    }}
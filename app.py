from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def get_weather():
    lat = os.getenv('LAT')
    lon = os.getenv('LON')
    openWeatherAPIKey = os.getenv('OPEN_WEATHER_API_KEY')

    openWeatherURL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openWeatherAPIKey}&units=imperial"

    resp = requests.get(openWeatherURL)
    weather = resp.json()

    return jsonify({
        "temp": weather["main"]["temp"],
        "feels_like": weather["main"]["feels_like"],
        "temp_max": weather["main"]["temp_max"],
        "temp_min": weather["main"]["temp_min"],
        "description": weather["weather"][0]["description"]
    })

@app.route("/api")
def get_updates():

    return get_weather()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
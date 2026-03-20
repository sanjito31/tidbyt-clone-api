import requests
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
from time import time
from io import BytesIO

load_dotenv()

weather_cache = None
weather_cache_last = 0
CACHE_TTL = 600

def get_weather():
    global weather_cache, weather_cache_last

    if weather_cache and (time() - weather_cache_last < CACHE_TTL):
        return weather_cache

    lat = os.getenv('LAT')
    lon = os.getenv('LON')
    api_key = os.getenv('OPEN_WEATHER_API_KEY')

    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

    resp = requests.get(open_weather_url)

    weather = resp.json()

    if resp.status_code == 200:
        weather_cache = {
            "temp": str(round(weather["main"]["temp"])),
            "feels_like": str(round(weather["main"]["feels_like"])),
            "temp_max": str(round(weather["main"]["temp_max"])),
            "temp_min": str(round(weather["main"]["temp_min"])),
            "description": str(weather["weather"][0]["description"])
        }
        weather_cache_last = time()

        return weather_cache
    else:
        return weather
    

def draw_weather():

    width = 64
    height = 32
    fontsize = 12
    fg = (255, 255, 255)

    weather = get_weather()

    text = weather["temp"] + " F"

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMonoNL-Regular.ttf", fontsize)
    except OSError:
        font = ImageFont.load_default(fontsize)

    bbox = draw.textbbox((0, 0), text, font=font)
    x = (width - bbox[2] + bbox[0]) // 2
    y = (height - bbox[3] + bbox[1]) // 2
    draw.text((x, y), text, font=font, fill=fg)

    buf = BytesIO()
    img.save(buf, "WEBP")
    return buf.getvalue()
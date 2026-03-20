from apps.AppBase import App
from utils.TimeKeeper import now
from utils.draw import draw_text, draw_weather
import requests

WEATHER_API_REQ_INTERVAL = 600  # 10 minutes

class WeatherApp(App):
    lat: str
    lon: str
    api_key: str
    
    cache: dict | None

    def __init__(self, lat, lon, api_key):
        super().__init__("weather", "Weather", ttl=WEATHER_API_REQ_INTERVAL)
        self.lat = lat
        self.lon = lon
        self.api_key = api_key
        self.api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=imperial" 
        self.cache = None


    def update(self):

        if self.cache and not self.is_stale(): return
        
        resp = requests.get(self.api_url)

        weather = resp.json()

        if resp.status_code == 200:
            self.cache = {
                "temp": str(round(weather["main"]["temp"])),
                "feels_like": str(round(weather["main"]["feels_like"])),
                "temp_max": str(round(weather["main"]["temp_max"])),
                "temp_min": str(round(weather["main"]["temp_min"])),
                "description": str(weather["weather"][0]["description"])
            }
            self.last_refreshed = now()
            return
        
    def render(self):
        if self.is_stale(): self.update()

        if self.cache:
            # return draw_text(text=self.cache["temp"]+"F")
            return draw_weather(weather=self.cache)
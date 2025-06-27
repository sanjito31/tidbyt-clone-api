from fastapi import FastAPI
from mta import getMTA_realtime
from weather import get_weather

app = FastAPI()

@app.get("/api/mta")
def mta_update():
    return getMTA_realtime()

@app.get("/api/weather")
def weather_update():
    return get_weather()
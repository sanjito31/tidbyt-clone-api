from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json

from weather import get_weather
from clock import get_time_str
from carousel import AppCarousel
from apps.TimeApp import TimeApp
from apps.WeatherApp import WeatherApp
from utils.draw import draw_time, draw_weather

from config import settings

from utils.draw import draw_text


app = FastAPI()
PORT = 8000

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

num_apps = 2
app_index = 0

@app.get("/api/test")
async def test():
    # global app_index

    # if app_index == 0:
    #     res = Response(content=draw_text(text=get_time_str(), align=('r', 'b')), media_type="image/webp")
    # else:
    #     res = Response(content=draw_text(text=(get_weather()["temp"] + "F"), align=('r', 'b') ), media_type="image/webp")

    # app_index = (app_index + 1) % num_apps
    # return res

    return Response(content=draw_weather({"temp": "54", "description": "sunny"}), media_type="image/webp")

# ----------------------------------------------
# Main Current Frame Endpoint
# ----------------------------------------------

carousel = AppCarousel([TimeApp(), 
                        WeatherApp(lat=settings.LAT, lon=settings.LON, api_key=settings.OPEN_WEATHER_API_KEY)
                        ])

@app.get("/api/current")
async def current():
    return Response(content=carousel.render_current(), media_type="image/webp")





LOG_FILE = "app.log"

class LogEntry(BaseModel):
    message: str
    time: datetime


@app.post("/api/logs", status_code=201)
async def logs(entry: LogEntry):
    with open(LOG_FILE, "a") as f:
        log = {
            "message": entry.message,
            "time": entry.time.isoformat()
        }
        f.write(json.dumps(log))
    return {"status": "logged"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)

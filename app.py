from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json

import spotify
from mta import getMTA_realtime
from weather import get_weather
import f1
import clock


app = FastAPI()
PORT = 8000

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "app.log"

class LogEntry(BaseModel):
    message: str
    time: datetime

@app.get("/api/current")
async def current():
    # return FileResponse("checkerboard.webp", media_type="image/webp")
    return Response(content=clock.draw_time(), media_type="image/webp")

@app.post("/api/logs", status_code=201)
async def logs(entry: LogEntry):
    with open(LOG_FILE, "a") as f:
        log = {
            "message": entry.message,
            "time": entry.time.isoformat()
        }
        f.write(json.dumps(log))
    return {"status": "logged"}


@app.get("/api/test")
async def test():
    return {"test": "this is a test api endpoint"}

@app.get("/api/mta")
def mta_update():
    return getMTA_realtime()

@app.get("/api/weather")
def weather_update():
    return get_weather()

@app.get("/api/spotify/currently-playing")
def spotify_playing():

    token = spotify.get_valid_user_token()

    if token is None:
        state = "currently-playing"
        ## kick off auth protocol
        return spotify.get_user_authorization(state=state)
    else:
        return {
            "spotify": {
                "currently_playing": spotify.get_currently_playing(token=token)
            }
        }


@app.get("/api/f1/drivers")
def f1_drivers():
    return f1.get_driver_standings()


@app.get("/api/f1/constructors")
def f1_constructors():
    return f1.get_constructor_standings()

@app.get("/spotify/callback")
def callback(request: Request):
    resp = spotify.callback(request)

    if resp["status"] == "error":
        raise HTTPException(status_code=resp["detail"]["status_code"], detail=resp["detail"]["message"])

    if resp["status"] == "success":
        spotify.save_tokens(resp["details"])

    return RedirectResponse(f"/api/spotify/{resp["state"]}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)

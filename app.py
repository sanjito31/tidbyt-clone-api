from fastapi import FastAPI, Request, HTTPException
from starlette.responses import RedirectResponse

import spotify
from mta import getMTA_realtime
from weather import get_weather
import f1

app = FastAPI()

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
        return spotify.get_currently_playing(token=token)


@app.get("api/f1/drivers")
def f1_drivers():
    return f1.get_driver_standings()


@app.get("api/f1/constructors")
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


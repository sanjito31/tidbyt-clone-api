from fastapi import FastAPI, Request, HTTPException
from starlette.responses import RedirectResponse

import spotify
from mta import getMTA_realtime
from weather import get_weather

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


    # if spotify.USER_AUTH_TOKEN is None:
    #     return RedirectResponse("/spotify/login", status_code=302)
    # else:
    #     header = {
    #         "Authorization": f"Bearer {spotify.USER_AUTH_TOKEN}"
    #     }
    #
    #     response =  requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=header)
    #     return response.json()

# @app.get("/spotify/login")
# def spotify_login():
#     return spotify.get_user_authorization()

@app.get("/spotify/callback")
def callback(request: Request):
    resp = spotify.callback(request)

    if resp["status"] == "error":
        raise HTTPException(status_code=resp["detail"]["status_code"], detail=resp["detail"]["message"])

    if resp["status"] == "success":
        spotify.save_tokens(resp["details"])

    return RedirectResponse(f"/api/spotify/{resp["state"]}")
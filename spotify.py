import urllib.parse
import os, json, time, base64, requests
from fastapi import Request
from dotenv import load_dotenv
from starlette.responses import RedirectResponse

load_dotenv()

TOKENS_PATH = os.path.join(os.path.dirname(__file__), '.spotify_tokens.json')
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
B64_CLIENT_SECRET = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("UTF-8")).decode("UTF-8")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
USER_AUTH_TOKEN = os.getenv("USER_AUTH_TOKEN")
# STATE = secrets.token_hex(8)
SCOPE = "user-library-read, user-read-currently-playing"

def load_tokens() -> dict:
    if os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, "r") as f:
            data = json.load(f)
        data.setdefault("expires_at", 0)
        return data
    return {
        "access_token": None,
        "expires_at": 0,
        "refresh_token": None
    }

def save_tokens(data):
    with open(TOKENS_PATH, 'w') as f:
        json.dump(data, f)
    return

def get_valid_user_token():
    tokens = load_tokens()
    now = time.time()
    if not tokens["access_token"]:
        # new login
        return None
        # get_user_authorization()
        # tokens = load_tokens()
    elif now > tokens["expires_at"]:
        # refresh token
        data = refresh_token(tokens["refresh_token"])
        save_tokens(data["details"])
        tokens = load_tokens()
    return tokens["access_token"]

def get_user_authorization(state: str):
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state
    }
    return RedirectResponse("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params))

def callback(request: Request) -> dict:

    code = request.query_params.get("code") if "code" in request.query_params else None
    state = request.query_params.get("state") if "state" in request.query_params else None
    error = request.query_params.get("error") if "error" in request.query_params else None

    print(code)
    if code is None:
        return {
            "status": "error",
            "details": {
                "message": "Access Denied: " + error,
                "status_code": "401"
            }
        }
    # if state != STATE:
    #     return {
    #         "status": "error",
    #         "details": {
    #             "message": "Invalid State",
    #             "status_code": "403"
    #         }
    #     }

    params = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": 'authorization_code'
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {B64_CLIENT_SECRET}"
    }

    response = requests.post("https://accounts.spotify.com/api/token", params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    expires_at = time.time() + data["expires_in"]

    return {
        "status": "success",
        "details": {
            "access_token": data["access_token"],
            "expires_at": expires_at,
            "refresh_token": data["refresh_token"]
        },
        "state": state
    }

def get_currently_playing(token):

    # user_auth_token = await get_valid_user_token()
    #
    # if type(user_auth_token) is RedirectResponse:
    #     return {
    #         "status": "error",
    #         "details": {
    #             "message": "Complete Login"
    #         }
    #     }
    # else:
    header = {
        "Authorization": f"Bearer {token}"
    }

    response =  requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=header)
    response.raise_for_status()

    if response.status_code == 204:
        return {
            "message": "nothing is currently playing"
        }
    return response.json()

def refresh_token(ref_tok: str) -> dict:
    params = {
        "grant_type": 'refresh_token',
        "refresh_token": ref_tok,
        "client_id": CLIENT_ID
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {B64_CLIENT_SECRET}"
    }

    response = requests.post("https://accounts.spotify.com/api/token", params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    expires_at = time.time() + data["expires_in"]


    return {
        "status": "success",
        "details": {
            "access_token": data["access_token"],
            "expires_at": expires_at,
            "refresh_token": data["refresh_token"]
        }
    }

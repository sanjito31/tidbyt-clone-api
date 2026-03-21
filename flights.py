import requests
import json
from config import settings
import math

def flights_above():
        lomax = float(settings.LOMAX)
        lomin = float(settings.LOMIN)
        latmin = float(settings.LATMIN)
        latmax = float(settings.LATMAX)

        OPENSKY_URL = f"https://opensky-network.org/api/states/all?lamin={latmin}&lomin={lomin}&lamax={latmax}&lomax={lomax}"

        resp = requests.get(OPENSKY_URL)
        flights = resp.json()
        req_time = flights["time"]

        if not flights["states"] or resp.status_code != 200: return None
        
        for i, flight in enumerate(flights["states"]):
                home = (float(settings.LON), float(settings.LAT))
                plane = (flight[5], flight[6])
                altitude = flight[13]
    
                flight.append(bearing(home, plane))
                flight.append(coord_dist(home, plane, altitude))

        flights = sorted(flights["states"].copy(), key=lambda x: x[-1])
        # print(flights)

        # ADSDB_AIR_URL = f"https://api.adsbdb.com/v0/aircraft/{flights[0][0]}"

        flight_info = None
        flight_obj = None
        for flight in flights:
            ADSDB_CALLSIGN_URL = f"https://api.adsbdb.com/v0/callsign/{flight[1].strip()}"
            resp = requests.get(ADSDB_CALLSIGN_URL).json()
            # print(resp)
            if isinstance(resp.get("response"), dict):
                   flight_obj = flight
                   flight_info = resp
                   break

        
        if flight_info is not None and flight_obj is not None:    
            return {
                    "flight_no": flight_info["response"]["flightroute"]["callsign"],
                    "airline": flight_info["response"]["flightroute"]["airline"]["name"],
                    "distance": flight_obj[-1],
                    "bearing": flight_obj[-2],
                    "origin": {
                            "code": flight_info["response"]["flightroute"]["origin"]["iata_code"],
                            "name": flight_info["response"]["flightroute"]["origin"]["name"],
                            "city": flight_info["response"]["flightroute"]["origin"]["municipality"],
                            "country": flight_info["response"]["flightroute"]["origin"]["country_name"]
                    },
                    "destination": {
                            "code": flight_info["response"]["flightroute"]["destination"]["iata_code"],
                            "name": flight_info["response"]["flightroute"]["destination"]["name"],
                            "city": flight_info["response"]["flightroute"]["destination"]["municipality"],
                            "country": flight_info["response"]["flightroute"]["destination"]["country_name"]
                    }
            }
        else:
               return None
        


def coord_dist(loc1, loc2, alt):
            METERS_PER_DEG = 111111
            dLat = (loc2[0] - loc1[0]) * METERS_PER_DEG
            dLon = (loc2[1] - loc1[1]) * METERS_PER_DEG * math.cos(loc1[0] * math.pi / 180)
            dist2d = math.sqrt(dLat**2 + dLon**2)
            if alt is None:
                   return dist2d
            return math.sqrt(dist2d**2 + alt**2)    

def bearing(loc1, loc2):
    dLat = (loc2[0] - loc1[0]) * 111111
    dLon = (loc2[1] - loc1[0]) * 111111 * math.cos(math.radians(loc1[0]))
    angle = math.degrees(math.atan2(dLon, dLat))
    return angle % 360         
                
                    

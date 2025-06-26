import requests
from google.transit import gtfs_realtime_pb2
# import pandas as pd
import json
import time

ROUTES_CSV_PATH = "./gtfs_subway/stops.txt"
BDFM_API_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"

MY_STATIONS = {
    "D22": "GRAND",
    "F15": "DELANCEY",
    "M18": "ESSEX"
}

DIRECTIONS = {
    "N": "UPTOWN",
    "S": "DOWNTOWN"
}

MY_LINES = [ "B", "D", "F", "M"]

# def get_my_stops():
#
#     stops = pd.read_csv(ROUTES_CSV_PATH)
#     my_stop_ids = tuple(MY_STATIONS.keys())
#     my_stops = stops[stops['stop_id'].str.startswith(my_stop_ids)]
#     return my_stops

def getMTA_realtime():

    now = int(time.time())

    feed = gtfs_realtime_pb2.FeedMessage()
    resp = requests.get(BDFM_API_URL)
    feed.ParseFromString(resp.content)

    rt_updates= {
        line: {
            "station": "",
            "uptown_waits": [],
            "downtown_waits": []
        }
        for line in MY_LINES
    }

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            tu = entity.trip_update
            line = tu.trip.route_id
            for stop in tu.stop_time_update:
                parent_stop = stop.stop_id[:-1]
                direction = stop.stop_id[-1]
                if parent_stop in tuple(MY_STATIONS.keys()):
                    wait = max(0, ((stop.arrival.time - now) // 60))
                    if wait > 30:
                        continue
                    rt_updates[f"{line}"]["station"] = MY_STATIONS[parent_stop]
                    if direction == "N":
                        rt_updates[f"{line}"]["uptown_waits"].append(wait)
                    else:
                        rt_updates[f"{line}"]["downtown_waits"].append(wait)

    for line in rt_updates.values():
        line["uptown_waits"].sort()
        line["downtown_waits"].sort()


    return rt_updates
import requests
from google.transit import gtfs_realtime_pb2
import pandas as pd

ROUTES_CSV_PATH = "./gtfs_subway/stops.txt"

MY_STATIONS = {
    "D22": "GRAND",
    "F15": "DELANCEY",
    "M18": "ESSEX"
}

def get_MTA():

    stops = pd.read_csv(ROUTES_CSV_PATH)
    my_stop_ids = tuple(MY_STATIONS.keys())
    my_stops = stops[stops['stop_id'].str.startswith(my_stop_ids)]


    
    






def getMTA_realtime():
    BDFM_API_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"

    feed = gtfs_realtime_pb2.FeedMessage()
    resp = requests.get(BDFM_API_URL)
    feed.ParseFromString(resp.content)
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            print(entity.trip_update)

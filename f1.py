import requests, json

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def get_driver_standings():

    wdc = { "f1_drivers": [] }
    resp = requests.get(BASE_URL + "/2025/driverstandings/")
    resp.raise_for_status()

    data = resp.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    for driver in data:
        wdc["f1_drivers"].append({
            "position": driver["position"],
            "givenName": driver["Driver"]["givenName"],
            "familyName": driver["Driver"]["familyName"],
            "points": driver["points"],
            "code": driver["Driver"]["code"],
            "team": driver["Constructors"][0]["name"]
        })

    # with open("f1_drivers.json", "w") as f:
    #     json.dump(wdc, f, indent=4)

    return wdc

def get_constructor_standings():
    wcc = { "f1_constructors": [] }
    resp = requests.get(BASE_URL + "/2025/constructorstandings/")
    resp.raise_for_status()
    data = resp.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

    for constructor in data:
        wcc["f1_constructors"].append({
            "position": constructor["position"],
            "points": constructor["points"],
            "name": constructor["Constructor"]["name"]
        })

    return wcc

wcc_data = get_constructor_standings()

with open("bin/constructor_standings.json", "w") as f:
    json.dump(wcc_data, f, indent=4)
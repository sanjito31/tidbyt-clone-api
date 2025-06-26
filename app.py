from flask import Flask
from mta import getMTA_realtime
from weather import get_weather
app = Flask(__name__)

@app.route("/api/mta")
def mta_update():
    return getMTA_realtime()

@app.route("/api/weather")
def weather_update():
    return get_weather()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
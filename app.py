from flask import Flask
from mta import get_MTA
from weather import get_weather

app = Flask(__name__)

@app.route("/api")
def get_updates():

    return get_weather()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
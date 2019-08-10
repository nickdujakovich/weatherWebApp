import requests
import APIKEY
from flask import Flask, request, render_template, url_for
from datetime import datetime

def callAPI(latlon = [37.8267,-122.4233]):
    url = "https://api.darksky.net/forecast/{}/{},{}".format(APIKEY.key, latlon[0], latlon[1])
    r = requests.get(url)
    json = r.json()
    return json

def getLatLon(location):
    url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(location,APIKEY.geocodeKey)
    r = requests.get(url)
    json = r.json()
    lat = json["results"][0]["geometry"]["lat"]
    lon = json["results"][0]["geometry"]["lng"]
    return [lat,lon, json]

app = Flask(__name__)
@app.route('/')
def hello_world():
    json = callAPI()
    return render_template('index.html', json = json)

@app.route('/', methods=['POST'])
def my_form_post():
    location = request.form['location']
    latlon = getLatLon(location)
    geocodeJson = latlon[2]
    json = callAPI(latlon)
    for forecast in json["daily"]["data"]:
        forecast["temperatureHigh"] = int(round(forecast["temperatureHigh"]))
        forecast["temperatureLow"] = int(round(forecast["temperatureLow"]))
        forecast["time"] = datetime.utcfromtimestamp(forecast["time"]).ctime()
        forecast["time"] = forecast["time"][:10] + forecast["time"][19:]
    icon = url_for('static', filename='{}.png'.format(json["currently"]["icon"]))
    return render_template('index2.html', json = json, location = location, geocodeJson = geocodeJson, icon = icon)

if __name__ == '__main__':
    app.run(debug=True)

    
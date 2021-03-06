import os
import requests
#import APIKEY
from flask import Flask, request, render_template, url_for
from datetime import datetime, timezone
import pendulum

locations = []

darkSkyKey = os.environ.get('darkSkyKey')
openCageDataKey = os.environ.get('openCageDataKey')

def callAPI(latlon = [37.8267,-122.4233]):
    url = "https://api.darksky.net/forecast/{}/{},{}".format(darkSkyKey, latlon[0], latlon[1])
    r = requests.get(url)
    json = r.json()
    return json

def getLatLon(location):
    url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(location,openCageDataKey)
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
    location = request.form.get('location', None)
    for dropdownLocation in locations:
        if(request.form.get('dropdownLocation', None) == dropdownLocation):
            location = dropdownLocation          
    latlon = getLatLon(location)
    geocodeJson = latlon[2]
    if(len(geocodeJson["results"][0]["formatted"]) > 39):
        geocodeJson["results"][0]["formatted"] = geocodeJson["results"][0]["formatted"][:39] + "..."
    if geocodeJson["results"][0]["formatted"] not in locations:
        locations.append(geocodeJson["results"][0]["formatted"])
    json = callAPI(latlon)
    


    json["currently"]["temperature"] = int(round(json["currently"]["temperature"]))
    for forecast in json["daily"]["data"]:
        forecast["temperatureHigh"] = int(round(forecast["temperatureHigh"]))
        forecast["temperatureLow"] = int(round(forecast["temperatureLow"]))
        forecast["time"] = pendulum.from_timestamp(forecast["time"], json["timezone"]).to_day_datetime_string()
        forecast["time"] = forecast["time"][:3] + forecast["time"][4:]
        forecast["time"] = forecast["time"].replace(" 12:00 AM", "")

    hourly = json["hourly"]["data"]
    for hourlyForecast in hourly:
        hourlyForecast["temperature"] = int(round(hourlyForecast["temperature"]))
        hourlyForecast["time"] = pendulum.from_timestamp(hourlyForecast["time"], json["timezone"]).to_datetime_string()
        hourlyForecast["time"] = datetime.strptime(hourlyForecast["time"][11:13], "%H").strftime("%I %p")
        if(hourlyForecast["time"][0] == '0'):
            hourlyForecast["time"] = hourlyForecast["time"][1:]

    icon = url_for('static', filename='{}.png'.format(json["currently"]["icon"]))
    return render_template('index2.html', json = json, location = location, geocodeJson = geocodeJson, icon = icon, hourly = hourly, locations = locations)

if __name__ == '__main__':
    app.run(debug=True)

    

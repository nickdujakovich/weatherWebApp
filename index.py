import requests
import APIKEY
from flask import Flask, request, render_template, url_for
from datetime import datetime, timezone
import pendulum

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
    zipped = zip(json["daily"]["data"], range(len(json["daily"]["data"])))
    return render_template('index2.html', json = json, location = location, geocodeJson = geocodeJson, icon = icon, zipped = zipped, hourly = hourly)

if __name__ == '__main__':
    app.run(debug=True)

    
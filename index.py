import requests
import APIKEY
from flask import Flask, request, render_template

def callAPI(latlon = [37.8267,-122.4233]):
    url = "https://api.darksky.net/forecast/{}/{},{}".format(APIKEY.key, latlon[0], latlon[1])
    r = requests.get(url)
    json = r.json()
    return json

def getLatLon(zipcode):
    url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(zipcode,APIKEY.geocodeKey)
    r = requests.get(url)
    json = r.json()
    lat = json["results"][0]["geometry"]["lat"]
    lon = json["results"][0]["geometry"]["lng"]
    return [lat,lon]

app = Flask(__name__)
@app.route('/')
def hello_world():
    json = callAPI()
    return render_template('index.html', json = json)

@app.route('/', methods=['POST'])
def my_form_post():
    zipcode = request.form['zipcode']
    latlon = getLatLon(zipcode)
    json = callAPI(latlon)
    return render_template('index.html', json = json, zipcode = zipcode)

if __name__ == '__main__':
    app.run(debug=True)

    
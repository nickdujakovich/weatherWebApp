import requests
import APIKEY
from flask import Flask, render_template
url = "https://api.darksky.net/forecast/{}/37.8267,-122.4233".format(APIKEY.key)
r = requests.get(url)
json = r.json()

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html', json = json)


if __name__ == '__main__':
    app.run()

    
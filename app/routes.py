from flask import  render_template, request
import requests
from app import app 
from datetime import datetime
import os

# OpenWeatherMap API endpoint and API key
API_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        params = {
            'q': city,
            'units': 'metric',
            'appid': API_KEY
        }
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()
        forecast = data['list']
        return render_template('results.html', forecast=forecast, city=city)
    return render_template('index.html')

@app.route('/day/<int:day>')
def day(day):
    city = request.args.get('city')
    params = {
        'q': city,
        'units': 'metric',
        'appid': API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    forecast = data['list']
    day_forecast = []
    for f in forecast:
        dt = datetime.strptime(f['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if dt.date() == datetime.strptime(forecast[day*8]['dt_txt'], '%Y-%m-%d %H:%M:%S').date():
            day_forecast.append(f)
    return render_template('day.html', day_forecast=day_forecast)
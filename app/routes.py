from flask import  render_template, request
import requests
from app import app 
from datetime import datetime
from config import OPENWEATHER_API_KEY
from collections import defaultdict

# OpenWeatherMap API endpoint and API key
API_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        params = {
            'q': city,
            'units': 'metric',
            'appid': OPENWEATHER_API_KEY
        }
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()
        forecast = data['list']
        for forecastData in forecast:
            forecastData['dt'] = forecastData['dt_txt'].split(" ")[0]

        weather_conditions = defaultdict(dict)
        for forecast_data in forecast:
            date = forecast_data['dt']
            condition = forecast_data['weather'][0]['main']
            if condition in weather_conditions[date]:
                weather_conditions[date][condition] += 1
            else:
                weather_conditions[date][condition] = 1

        most_frequent_conditions = {}
        for date, conditions in weather_conditions.items():
            most_frequent_conditions[date] = max(conditions, key=conditions.get)

        return render_template('results.html', forecast=forecast, city=city, most_frequent_conditions=most_frequent_conditions)
    return render_template('index.html')

@app.route('/day/<int:day>')
def day(day):
    city = request.args.get('city')
    params = {
        'q': city,
        'units': 'metric',
        'appid': OPENWEATHER_API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    forecast = data['list']
    day_forecast = []
    for f in forecast:
        dt = datetime.strptime(f['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if dt.date() == datetime.strptime(forecast[day*8]['dt_txt'], '%Y-%m-%d %H:%M:%S').date():
            f['today'] = dt.date()
            f['time'] = dt.time()
            day_forecast.append(f)
            print(f)
            print(' ')
    return render_template('day.html', day_forecast=day_forecast)
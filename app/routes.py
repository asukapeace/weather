from flask import  render_template, request
import requests
from app import app 

# OpenWeatherMap API endpoint and API key
API_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "fb9578485cc0abe067911665f4254efb"

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
    day_data = forecast[day*8]  # OpenWeatherMap API returns 8 forecasts per day
    return render_template('day.html', day_data=day_data)

if __name__ == '__main__':
    app.run(debug=True)
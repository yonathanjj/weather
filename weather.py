from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    hourly_forecast = None

    if request.method == 'POST':
        api_key = '4488b8b57b6949f49f141e0acdc2ac68'
        location = request.form['location']

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            wind_direction = data['wind']['deg']

            weather_data = {
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction
            }

            # Fetch hourly forecast
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            hourly_data = response.json()
            if hourly_data['cod'] == '200':
                hourly_forecast = hourly_data['list']

    return render_template('weather.html', weather_data=weather_data, hourly_forecast=hourly_forecast)

if __name__ == '__main__':
    app.run(debug=True)
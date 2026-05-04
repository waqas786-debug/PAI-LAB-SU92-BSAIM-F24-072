import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather_dashboard():
    weather_report = None
    if request.method == 'POST':
        target_city = request.form.get('city_name')
        # OpenWeatherMap API key replace karein
        api_key = "YOUR_API_KEY_HERE"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={target_city}&appid={api_key}&units=metric"
        
        try:
            api_response = requests.get(base_url)
            if api_response.status_code == 200:
                weather_report = api_response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")

    return render_template('view.html', info=weather_report)

if __name__ == '__main__':
    app.run(port=8080)
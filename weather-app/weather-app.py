from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_KEY = "ea741695c2d9883c2ba820c91837e745"

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
</head>
<body>
    <h2>Weather App</h2>
    <form method="post">
        Enter City: <input type="text" name="city" required>
        <input type="submit" value="Get Weather">
    </form>

    {% if weather %}
        <h3>City: {{ weather.city }}</h3>
        <p>Temperature: {{ weather.temp }} °C</p>
        <p>Weather: {{ weather.description }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None

    if request.method == 'POST':
        city = request.form['city']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get('cod') == 200:
            weather_data = {
                'city': data['name'],
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description']
            }
        else:
            weather_data = {
                'city': city,
                'temp': 'N/A',
                'description': 'City not found'
            }

    return render_template_string(html_page, weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)

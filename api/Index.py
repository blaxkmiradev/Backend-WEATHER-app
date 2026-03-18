from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Allow your specific Vercel frontend URL or use '*' for testing
CORS(app)


API_KEY = os.environ.get("OPENWEATHER_API_KEY")

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "No city"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    return jsonify({
        "name": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    })


def handler(event, context):
    return app(event, context)
    

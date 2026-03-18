from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Enable CORS so your React app can talk to it
CORS(app)

# Add your Key in Vercel Dashboard Environment Variables
API_KEY = os.environ.get("WEATHER_API_KEY")

@app.route('/api/index', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "No city provided"}), 400

    # Handle encoding (like spaces in Phnom Penh) automatically via requests
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "City not found")}), response.status_code

        return jsonify({
            "name": data["name"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel
def handler(event, context):
    return app(event, context)
    

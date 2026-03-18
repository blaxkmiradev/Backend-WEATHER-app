from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# OpenWeather API Key (Set this in Vercel Dashboard!)
API_KEY = os.environ.get("WEATHER_API_KEY")

# We define multiple routes to ensure the 404 disappears
@app.route('/')
@app.route('/api')
@app.route('/api/index')
def weather_api():
    city = request.args.get('city')
    if not city:
        return jsonify({"message": "Backend is Online", "usage": "/api/index?city=London"}), 200

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
            "wind": data["wind"]["speed"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel needs the 'app' object, but this allows local testing
if __name__ == "__main__":
    app.run(debug=True)
    

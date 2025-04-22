from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# In-memory user database
users = {}

# Your OpenWeather API key
API_KEY = "72524226a15b891c77fb4434c5a92dd7"

# AQI categories
AQI_CATEGORIES = {
    1: ("Good", "#00E400"),
    2: ("Fair", "#9CFF9C"),
    3: ("Moderate", "#FFFF00"),
    4: ("Poor", "#FF7E00"),
    5: ("Very Poor", "#FF0000")
}


@app.route('/')
def index():
    return send_file('home.html')
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"message": "User already exists"}), 400

    users[email] = password
    return jsonify({"message": "Registration successful"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if users.get(email) != password:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200

@app.route('/get_aqi', methods=['GET'])  # ✅ Changed from POST to GET
def get_aqi():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"message": "Latitude and Longitude required"}), 400

    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        aqi_data = response.json()
        aqi_index = aqi_data["list"][0]["main"]["aqi"]
        category, color = AQI_CATEGORIES.get(aqi_index, ("Unknown", "#999"))

        return jsonify({
            "aqi_index": aqi_index,
            "aqi_category": category,
            "color": color
        })
    else:
        return jsonify({"message": "Failed to get AQI data"}), 500

if __name__ == '__main__':
    app.run(debug=True)

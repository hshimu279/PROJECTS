from flask import Flask, render_template, request
import requests
import folium

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"   # Replace with your StormGlass API Key
API_URL = "https://api.stormglass.io/v2/weather/point"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    map_html = None

    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")

        headers = {"Authorization": API_KEY}
        params = {
            "lat": lat,
            "lng": lon,
            "params": "waveHeight,windSpeed,windDirection,currentSpeed,airTemperature"
        }
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if "hours" in data:
                weather_data = data["hours"][0]

            m = folium.Map(location=[lat, lon], zoom_start=6)
            folium.Marker([lat, lon], popup="Selected Location").add_to(m)
            map_html = m._repr_html_()
        else:
            weather_data = {"error": "API Error – Check API Key"}

    return render_template("index.html", weather=weather_data, map_html=map_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

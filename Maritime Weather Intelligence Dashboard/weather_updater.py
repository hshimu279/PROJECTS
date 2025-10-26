import pandas as pd
import requests
import time
import os

API_KEY = "b4867d695d9a8a2b8825cc0a025cf1c2"   # 👈 Put API here
INPUT_FILE = "final.csv"                     # Ports master file
OUTPUT_FOLDER = "weather_by_country"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None

def update_weather():
    df = pd.read_csv(INPUT_FILE)

    for country in df["country"].dropna().unique():
        country_ports = df[df["country"].str.strip().str.lower() == country.strip().lower()]
        results = []

        for _, row in country_ports.iterrows():
            weather = fetch_weather(row["lat"], row["lon"])
            if weather:
                wind_speed = weather["wind"]["speed"]
                desc = weather["weather"][0]["description"].capitalize()

                # classify safety
                if any(word in desc.lower() for word in ["storm", "hurricane", "cyclone", "tornado"]):
                    status = "🚨 Worst"
                elif wind_speed < 5:
                    status = "✅ Safe"
                elif wind_speed < 10:
                    status = "⚠ Moderate"
                elif wind_speed < 20:
                    status = "⚡ Dangerous"
                else:
                    status = "🚨 Worst"

                results.append({
                    "Port": row["name"],
                    "Country": row["country"],
                    "Latitude": row["lat"],
                    "Longitude": row["lon"],
                    "Temperature (°C)": weather["main"]["temp"],
                    "Weather": desc,
                    "Wind (m/s)": wind_speed,
                    "Safety Status": status,
                    "Updated_At": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                results.append({
                    "Port": row["name"],
                    "Country": row["country"],
                    "Latitude": row["lat"],
                    "Longitude": row["lon"],
                    "Temperature (°C)": None,
                    "Weather": "No Data",
                    "Wind (m/s)": None,
                    "Safety Status": "❓ Unknown",
                    "Updated_At": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            time.sleep(1)  # avoid hitting API rate limit

        # Save per-country CSV
        out_file = os.path.join(OUTPUT_FOLDER, country.strip().lower().replace(" ", "_") + ".csv")
        pd.DataFrame(results).to_csv(out_file, index=False)
        print(f"✅ Updated {out_file}")

if __name__ == "__main__":
    update_weather()

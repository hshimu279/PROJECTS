pip install streamlit_folium
pip install folium
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Maritime Weather Intelligence Dashboard", layout="wide")

st.title(" Maritime Weather Intelligence Dashboard")

# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.header("⚙ Settings")

# Folder where per-country weather CSVs are stored
CSV_FOLDER = "weather_by_country"

if not os.path.exists(CSV_FOLDER):
    st.error(" No weather data folder found. Please run the updater script first.")
    st.stop()

# List available countries (based on CSV files)
all_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]
if not all_files:
    st.error(" No country CSV files found in weather_by_country/.")
    st.stop()

all_countries = [f.replace(".csv", "").replace("_", " ").title() for f in all_files]

# Select country
selected_country = st.sidebar.selectbox(" Select Country", sorted(all_countries))

# -----------------------------
# Load Data for Selected Country
# -----------------------------
file_path = os.path.join(
    CSV_FOLDER, selected_country.replace(" ", "_").lower() + ".csv"
)

@st.cache_data
def load_country_weather(path):
    return pd.read_csv(path)

df_results = load_country_weather(file_path)

# -----------------------------
# Show Port Weather Table
# -----------------------------
st.subheader(f"Port Weather Status - {selected_country}")

if df_results.empty:
    st.warning(f"No port data available for {selected_country}")
else:
    # Color-coded table
    def color_safety(val):
        if isinstance(val, str):
            if "Safe" in val:
                return "background-color: lightgreen"
            elif "Moderate" in val:
                return "background-color: khaki"
            elif "Dangerous" in val:
                return "background-color: orange"
            elif "Worst" in val:
                return "background-color: red; color: white"
        return ""

    st.dataframe(
        df_results.style.applymap(color_safety, subset=["Safety Status"]),
        use_container_width=True,
    )

    # Download option
    st.download_button(
        " Download Results as CSV",
        df_results.to_csv(index=False),
        f"{selected_country.lower().replace(' ', '_')}_weather.csv",
        "text/csv",
    )

    # -----------------------------
    # Ports Map
    # -----------------------------
    st.subheader(f" Ports Map - {selected_country}")

    if not df_results.empty:
        m = folium.Map(
            location=[df_results.iloc[0]["Latitude"], df_results.iloc[0]["Longitude"]],
            zoom_start=4,
        )

        for _, row in df_results.iterrows():
            emoji = row["Safety Status"].split()[0] if isinstance(row["Safety Status"], str) else "❓"

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"{emoji} <b>{row['Port']}</b> ({row['Country']})<br>"
                      f" {row['Temperature (°C)']} °C<br>"
                      f" {row['Wind (m/s)']} m/s<br>"
                      f"{row['Safety Status']}<br>"
                      f"⏱ Updated: {row['Updated_At']}",
                tooltip=f"{emoji} {row['Port']}",
                icon=folium.Icon(
                    color="red"
                    if "Worst" in row["Safety Status"]
                    else "orange"
                    if "Dangerous" in row["Safety Status"]
                    else "lightgray"
                    if "Moderate" in row["Safety Status"]
                    else "green"
                ),
            ).add_to(m)

        st_folium(m, width=800, height=500)


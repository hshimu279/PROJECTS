import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Maritime Weather Intelligence Dashboard",
    layout="wide"
)

st.title("Maritime Weather Intelligence Dashboard")

# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.header("⚙ Settings")

# Folder where per-country weather CSVs are stored
CSV_FOLDER = "weather_by_country"

if not os.path.exists(CSV_FOLDER):
    st.error("No weather data folder found. "
             "Make sure the 'weather_by_country' folder is in the same directory as app.py.")
    st.stop()

# List available countries (based on CSV files)
all_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]
if not all_files:
    st.error("No country CSV files found in weather_by_country/.")
    st.stop()

# Convert filenames like "united_states.csv" → "United States"
def filename_to_country(name: str) -> str:
    return name.replace(".csv", "").replace("_", " ").title()

all_countries = [filename_to_country(f) for f in all_files]

# Select country
selected_country = st.sidebar.selectbox("Select Country", sorted(all_countries))

# -----------------------------
# Load Data for Selected Country
# -----------------------------
file_path = os.path.join(
    CSV_FOLDER,
    selected_country.replace(" ", "_").lower() + ".csv"
)

@st.cache_data
def load_country_weather(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

df_results = load_country_weather(file_path)

# -----------------------------
# Show Port Weather Table
# -----------------------------
st.subheader(f"Port Weather Status - {selected_country}")

if df_results.empty:
    st.warning(f"No port data available for {selected_country}")
else:
    # Color-coded table based on "Safety Status" column
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

    if "Safety Status" in df_results.columns:
        styled_df = df_results.style.applymap(color_safety, subset=["Safety Status"])
    else:
        styled_df = df_results  # no styling if column missing

    st.dataframe(styled_df, use_container_width=True)

    # Download option
    st.download_button(
        "Download Results as CSV",
        df_results.to_csv(index=False),
        file_name=f"{selected_country.lower().replace(' ', '_')}_weather.csv",
        mime="text/csv",
    )

    # -----------------------------
    # Ports Map
    # -----------------------------
    st.subheader(f"Ports Map - {selected_country}")

    if "Latitude" in df_results.columns and "Longitude" in df_results.columns:
        # Center map on first row
        m = folium.Map(
            location=[df_results.iloc[0]["Latitude"], df_results.iloc[0]["Longitude"]],
            zoom_start=4,
        )

        for _, row in df_results.iterrows():
            lat = row.get("Latitude")
            lon = row.get("Longitude")

            if pd.isna(lat) or pd.isna(lon):
                continue

            status = row.get("Safety Status", "")
            emoji = status.split()[0] if isinstance(status, str) and status else "❓"

            # Choose marker color
            if isinstance(status, str):
                if "Worst" in status:
                    color = "red"
                elif "Dangerous" in status:
                    color = "orange"
                elif "Moderate" in status:
                    color = "lightgray"
                else:
                    color = "green"
            else:
                color = "blue"

            popup_html = (
                f"{emoji} <b>{row.get('Port', 'Unknown Port')}</b> "
                f"({row.get('Country', selected_country)})<br>"
                f"🌡 {row.get('Temperature (°C)', 'N/A')} °C<br>"
                f"💨 {row.get('Wind (m/s)', 'N/A')} m/s<br>"
                f"⚠ {status}<br>"
                f"⏱ Updated: {row.get('Updated_At', 'N/A')}"
            )

            folium.Marker(
                location=[lat, lon],
                popup=popup_html,
                tooltip=f"{emoji} {row.get('Port', 'Port')}",
                icon=folium.Icon(color=color),
            ).add_to(m)

        st_folium(m, width=900, height=550)
    else:
        st.warning("Latitude/Longitude columns not found in the data. Map cannot be displayed.")

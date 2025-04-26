import streamlit as st
st.set_page_config(page_title="Life Track Dashboard", layout="wide")

from eda.weather_eda import show_weather_dashboard, load_weather_data
from eda.spotify_eda import show_spotify_dashboard, load_spotify_data

# Load data upfront
weather_df = load_weather_data()
spotify_df = load_spotify_data()

# Sidebar
st.sidebar.title("📊 Life Track")
selected = st.sidebar.radio("Choose Dashboard", ["Weather", "Spotify"])

# Show selected dashboard
if selected == "Weather":
    show_weather_dashboard(weather_df)
elif selected == "Spotify":
    show_spotify_dashboard(spotify_df)
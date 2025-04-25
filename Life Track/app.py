import streamlit as st
import altair as alt
import time
from datetime import timedelta
import pandas as pd
from eda.weather_eda import show_weather_dashboard
from eda.spotify_eda import show_spotify_dashboard

# Load data
weather_df = pd.read_csv("merged_weather_data.csv", parse_dates=["datetime"])
spotify_df = pd.read_csv("spotify_streaming_cleaned.csv", parse_dates=["endTime"])

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Weather", "Spotify"])

# Routing logic
if page == "Weather":
    show_weather_dashboard(weather_df)
elif page == "Spotify":
    show_spotify_dashboard(spotify_df)

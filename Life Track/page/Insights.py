import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="📊 Insights", layout="wide")
st.title("📊 Insights")
st.markdown("Explore your listening habits and how they sync with time, moods, and weather.")

# --- Load Data ---
@st.cache_data
def load_data():
    spotify_df = pd.read_csv("data/spotify_data.csv", parse_dates=['date'])
    weather_df = pd.read_csv("data/weather_data.csv", parse_dates=['date'])
    return spotify_df, weather_df

spotify_df, weather_df = load_data()

# --- Date Filter ---
start_date, end_date = st.date_input(
    "Select a time range:",
    value=(spotify_df['date'].min(), spotify_df['date'].max())
)

spotify_filtered = spotify_df[(spotify_df['date'] >= pd.to_datetime(start_date)) & (spotify_df['date'] <= pd.to_datetime(end_date))]
weather_filtered = weather_df[(weather_df['date'] >= pd.to_datetime(start_date)) & (weather_df['date'] <= pd.to_datetime(end_date)) & (weather_df['city'].str.lower().str.strip() == 'berlin')]

# --- Listening Over Time ---
st.subheader("🎧 Total Listening Time Over Time")
daily_listening = spotify_filtered.groupby('date')['msPlayed'].sum() / 60000  # ms to minutes
st.line_chart(daily_listening.rename("Minutes Listened"))

# --- Genre Trends ---
st.subheader("🎶 Genre Trends")
genre_time = spotify_filtered.groupby(['date', 'main_genre'])['msPlayed'].sum().div(60000).reset_index()
genre_pivot = genre_time.pivot(index='date', columns='main_genre', values='msPlayed').fillna(0)
st.area_chart(genre_pivot)

# --- Weather vs Listening ---
st.subheader("☁️ Weather vs Listening Time")
merged = pd.merge(
    spotify_filtered.groupby('date')['msPlayed'].sum().div(60000).reset_index(name='minutes'),
    weather_filtered.groupby('date')[['temp']].mean().reset_index(),
    on='date',
    how='inner'
)
st.line_chart(merged.set_index('date'))

# --- Genre Filter ---
st.subheader("🎛️ Explore by Genre")
all_genres = spotify_filtered['main_genre'].dropna().unique()
genre_choice = st.selectbox("Choose a genre to explore:", options=sorted(all_genres))
genre_df = spotify_filtered[spotify_filtered['main_genre'] == genre_choice]
genre_trend = genre_df.groupby('date')['msPlayed'].sum().div(60000)
st.line_chart(genre_trend.rename(f"Listening Time: {genre_choice}"))

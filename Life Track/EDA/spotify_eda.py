import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

def load_spotify_data():
    spotify_df = pd.read_csv("spotify_streaming_cleaned.csv")  # 👈 replace with your file
    spotify_df["datetime"] = pd.to_datetime(spotify_df["datetime"])
    return spotify_df

def show_spotify_dashboard(spotify_df):
    today = pd.to_datetime(date.today())
    spotify_df["datetime"] = pd.to_datetime(spotify_df["endTime"])

    st.title("🎧 Spotify Listening Dashboard")

    # --- Songs Today
    st.subheader("Total Songs Today")
    today_df = spotify_df[spotify_df["datetime"].dt.date == today.date()]
    st.metric("Total Songs Played", len(today_df))

    # --- Top 5 Artists
    st.subheader("Top 5 Artists Today")
    top_artists = today_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(5)
    st.bar_chart(top_artists)

    # --- Top 5 Genres
    st.subheader("Top 5 Genres Today")
    if "main_genre" in spotify_df.columns:
        top_genres = today_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_genres)
    else:
        st.write("No genre data available.")

    # --- Listening Trend by Hour
    st.subheader("Listening Trend Throughout the Day")
    today_df["hour"] = today_df["datetime"].dt.hour
    hourly = today_df.groupby("hour")["msPlayed"].count().reset_index()
    line = alt.Chart(hourly).mark_line(point=True).encode(
        x="hour:O", y="msPlayed:Q", tooltip=["hour", "msPlayed"]
    ).properties(title="Songs Played by Hour")
    st.altair_chart(line, use_container_width=True)
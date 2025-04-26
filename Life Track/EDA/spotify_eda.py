# --- Imports ---
import streamlit as st
import pandas as pd
import altair as alt
import time
from datetime import datetime
from streamlit_lottie import st_lottie
import requests

# --- Custom Local CSS for Styling ---
def local_css():
    st.markdown("""
        <style>
            .centered-title {
                text-align: center;
                font-size: 40px;
                color: #39FF14;
                text-shadow: 0px 0px 10px #39FF14;
            }
            .stProgress > div > div > div > div {
                background-color: #00FF00;
                box-shadow: 0 0 10px #00FF00;
            }
            div.stButton > button {
                background-color: #1DB954;
                color: white;
                border-radius: 10px;
                height: 50px;
                font-size: 20px;
            }
            div.stButton > button:hover {
                background-color: #1ed760;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Lottie animation loader ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Load Spotify Data ---
def load_spotify_data():
    spotify_df = pd.read_csv("spotify_streaming_cleaned.csv")
    spotify_df["datetime"] = pd.to_datetime(spotify_df["endTime"])
    spotify_df["date"] = spotify_df["datetime"].dt.date
    spotify_df["month"] = spotify_df["datetime"].dt.month
    spotify_df["year"] = spotify_df["datetime"].dt.year

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    spotify_df["season"] = spotify_df["month"].apply(get_season)
    return spotify_df

# --- Dashboard ---
def show_spotify_dashboard(spotify_df):
    local_css()

    # --- Splash Animation ---
    lottie_spotify = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_TvW70w.json")
    if lottie_spotify:
        st_lottie(lottie_spotify, height=250)

    # --- Title ---
    st.markdown('<h1 class="centered-title">🎷 Spotify Listening Dashboard</h1>', unsafe_allow_html=True)

    # --- Current Season ---
    today = datetime.today()
    current_month = today.month
    current_season = ("Winter" if current_month in [12,1,2] else
                      "Spring" if current_month in [3,4,5] else
                      "Summer" if current_month in [6,7,8] else
                      "Autumn")
    st.success(f"🌿 Current Season: {current_season}")

    # --- Date Selector ---
    available_dates = sorted(spotify_df["date"].unique(), reverse=True)
    selected_date = st.selectbox(
        "Choose a date to explore:", 
        available_dates, 
        index=0, 
        format_func=lambda x: pd.to_datetime(x).strftime('%A, %B %d')
    )

    daily_df = spotify_df[spotify_df["date"] == selected_date]

    st.subheader(f"🎼 Listening Summary for {pd.to_datetime(selected_date).strftime('%A, %B %d')}")
    st.metric("Total Songs Played", len(daily_df))

    # --- Top 5 Artists ---
    st.subheader("Top 5 Artists")
    top_artists = daily_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(5).reset_index()
    artists_chart = alt.Chart(top_artists).mark_bar(color="green").encode(
        x=alt.X("artistName:N", title="Artist", sort='-y'),
        y=alt.Y("msPlayed:Q", title="Songs Played"),
        tooltip=["artistName", "msPlayed"]
    ).properties(title="Top 5 Artists")
    st.altair_chart(artists_chart, use_container_width=True)

    # --- Top 5 Genres ---
    st.subheader("Top 5 Genres")
    if "main_genre" in daily_df.columns:
        top_genres = daily_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        genres_chart = alt.Chart(top_genres).mark_bar(color="green").encode(
            x=alt.X("main_genre:N", title="Genre", sort='-y'),
            y=alt.Y("msPlayed:Q", title="Total Listening (ms)"),
            tooltip=["main_genre", "msPlayed"]
        ).properties(title="Top 5 Genres")
        st.altair_chart(genres_chart, use_container_width=True)
    else:
        st.info("No genre data available.")

    # --- Animated Hourly Listening Trend ---
    st.subheader("🎬 Animated Hourly Listening Trend")

    # Prepare hourly data
    hourly_df = daily_df.copy()
    hourly_df["hour"] = hourly_df["datetime"].dt.hour
    full_hours = pd.DataFrame({"hour": list(range(24))})
    hourly_counts = hourly_df.groupby("hour")["msPlayed"].count().reset_index().rename(columns={"msPlayed": "count"})
    hourly_complete = pd.merge(full_hours, hourly_counts, on="hour", how="left").fillna(0)

    # --- State Management
    if "play_animation" not in st.session_state:
        st.session_state.play_animation = False
    if "hour_counter" not in st.session_state:
        st.session_state.hour_counter = 0

    # --- Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Animation"):
            st.session_state.play_animation = True
            st.session_state.hour_counter = 0
    with col2:
        if st.button("⏹️ Stop Animation"):
            st.session_state.play_animation = False

    # --- Placeholders for live update
    chart_placeholder = st.empty()
    progress_placeholder = st.empty()

    # --- Animate if playing
    if st.session_state.play_animation:
        for hr in range(st.session_state.hour_counter, 24):
            st.session_state.hour_counter = hr
            
            # Update progress
            progress_placeholder.progress((hr+1)/24, text=f"Loading hour {hr+1}/24...")

            # Update chart
            animated_chart = alt.Chart(hourly_complete[hourly_complete["hour"] <= hr]).mark_line(
                point=True, interpolate='monotone', color="green"  # smoother line
            ).encode(
                x=alt.X("hour:O", title="Hour of Day"),
                y=alt.Y("count:Q", title="Songs Played"),
                tooltip=["hour", "count"]
            ).properties(title="🎥 Songs Played by Hour (Auto-Playing)")
            chart_placeholder.altair_chart(animated_chart, use_container_width=True)

            time.sleep(0.4)

        st.session_state.play_animation = False

    else:
        # Show static chart if not animating
        animated_chart = alt.Chart(hourly_complete[hourly_complete["hour"] <= st.session_state.hour_counter]).mark_line(
            point=True, interpolate='monotone', color="green"
        ).encode(
            x=alt.X("hour:O", title="Hour of Day"),
            y=alt.Y("count:Q", title="Songs Played"),
            tooltip=["hour", "count"]
        ).properties(title="🎥 Songs Played by Hour (Paused)")
        chart_placeholder.altair_chart(animated_chart, use_container_width=True)

    # --- Static Hourly Trend ---
    st.subheader("⏰ Hourly Listening Trend")
    hourly_line_chart = alt.Chart(hourly_complete).mark_line(point=True, color="green").encode(
        x=alt.X("hour:O", title="Hour of Day"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["hour", "count"]
    ).properties(title="🎵 Songs Played by Hour")
    st.altair_chart(hourly_line_chart, use_container_width=True)

    # --- Radial Clock View ---
    st.subheader("🕰️ Hourly Listening Radial Clock")
    radial_chart = alt.Chart(hourly_complete).mark_arc(innerRadius=50, outerRadius=150).encode(
        theta=alt.Theta("count:Q", stack=True),
        color=alt.Color("hour:O", scale=alt.Scale(scheme="greens")),
        tooltip=["hour", "count"]
    ).properties(title="Songs Played by Hour (Radial View)")
    st.altair_chart(radial_chart, use_container_width=True)

    # --- Monthly Listening Trends ---
    st.subheader("🌿 Monthly Listening Trends")
    monthly_df = spotify_df.groupby(["year", "month"]).size().reset_index(name="count")
    monthly_df["date"] = pd.to_datetime(monthly_df[["year", "month"]].assign(day=1))

    monthly_chart = alt.Chart(monthly_df).mark_area(color="green", interpolate="monotone").encode(
        x=alt.X("date:T", title="Month"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["year", "month", "count"]
    ).properties(title="Monthly Listening Trends")
    st.altair_chart(monthly_chart, use_container_width=True)

    # --- Weekly Listening Trend ---
    st.subheader("🌅 Weekly Listening Trend")
    weekly_df = spotify_df.copy()
    weekly_df["week"] = weekly_df["datetime"].dt.isocalendar().week
    week_trend = weekly_df.groupby("week").size().reset_index(name="count")

    week_chart = alt.Chart(week_trend).mark_line(point=True, color="orange").encode(
        x=alt.X("week:O", title="Week of the Year"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["week", "count"]
    ).properties(title="Weekly Songs Played")
    st.altair_chart(week_chart, use_container_width=True)

    # --- Top 10 Artists (All Time) ---
    st.subheader("🎶 Top 10 Most Popular Artists (All Time)")
    top10_artists = spotify_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(10).reset_index()

    top10_chart = alt.Chart(top10_artists).mark_bar(color="pink").encode(
        x=alt.X("msPlayed:Q", title="Total Listening (ms)"),
        y=alt.Y("artistName:N", sort='-x', title="Artist"),
        tooltip=["artistName", "msPlayed"]
    ).properties(title="Top 10 Most Popular Artists (All Time)")
    st.altair_chart(top10_chart, use_container_width=True)

    # --- Pie Chart: Listening by Season ---
    st.subheader("🌎 Overall Listening by Season")
    season_summary = spotify_df.groupby("season")["msPlayed"].sum().reset_index()
    season_summary["percent"] = (season_summary["msPlayed"] / season_summary["msPlayed"].sum()) * 100

    pie_chart = alt.Chart(season_summary).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="msPlayed", type="quantitative"),
        color=alt.Color(field="season", type="nominal"),
        tooltip=[alt.Tooltip("season:N"), alt.Tooltip("percent:Q", format=".2f")]
    ).properties(title="Season Share of Total Listening")
    st.altair_chart(pie_chart, use_container_width=True)

# --- Main Run ---
if __name__ == "__main__":
    spotify_df = load_spotify_data()
    show_spotify_dashboard(spotify_df)

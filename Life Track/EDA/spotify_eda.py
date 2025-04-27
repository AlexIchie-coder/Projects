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
def load_lottieurl(url:str):
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
            return "❄️ Winter"
        elif month in [3, 4, 5]:
            return "🌸 Spring"
        elif month in [6, 7, 8]:
            return "☀️ Summer"
        else:
            return "🍂 Autumn"

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

    def get_season(month):
        if month in [12, 1, 2]:
            return "❄️ Winter"
        elif month in [3, 4, 5]:
            return "🌸 Spring"
        elif month in [6, 7, 8]:
            return "☀️ Summer"
        else:
            return "🍂 Autumn"

    current_season = get_season(current_month)
    
    st.markdown(f"<h2 style='text-align: center; color: #1DB954;'>{current_season}</h2>", unsafe_allow_html=True)

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

# --- Animated Hourly Listening Trend with Auto-Reverse ---
    st.subheader("Hourly Listening Trend")

    # Prepare hourly data
    hourly_df = daily_df.copy()
    hourly_df["hour"] = hourly_df["datetime"].dt.hour
    full_hours = pd.DataFrame({"hour": list(range(24))})
    hourly_counts = hourly_df.groupby("hour")["msPlayed"].count().reset_index().rename(columns={"msPlayed": "count"})
    hourly_complete = pd.merge(full_hours, hourly_counts, on="hour", how="left").fillna(0)

    # Initialize session state
    if "hour_counter" not in st.session_state:
        st.session_state.hour_counter = 0
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "forward" not in st.session_state:
        st.session_state.forward = True  # Direction of animation

    # --- Play / Stop Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Play Animation"):
            st.session_state.playing = True
    with col2:
        if st.button("⏹ Stop Animation"):
            st.session_state.playing = False

    placeholder = st.empty()

    if st.session_state.playing:
        progress_bar = st.progress(0)
        total_steps = 24

        while st.session_state.playing:
            current_data = hourly_complete[hourly_complete["hour"] <= st.session_state.hour_counter]

            animated_chart = alt.Chart(current_data).mark_line(
                interpolate='monotone',
                point=True,
                color="green"
            ).encode(
                x=alt.X("hour:O", title="Hour of Day"),
                y=alt.Y("count:Q", title="Songs Played"),
                tooltip=["hour", "count"]
            ).properties(title="🎥 Songs Played by Hour (Auto-Playing)")

            placeholder.altair_chart(animated_chart, use_container_width=True)

            # Update progress
            progress = int((st.session_state.hour_counter / (total_steps - 1)) * 100)
            progress_bar.progress(progress)

            # Move counter
            if st.session_state.forward:
                st.session_state.hour_counter += 1
                if st.session_state.hour_counter >= 23:
                    st.session_state.forward = False  # Switch to reverse
            else:
                st.session_state.hour_counter -= 1
                if st.session_state.hour_counter <= 0:
                    st.session_state.forward = True  # Switch to forward

            time.sleep(0.2)

        progress_bar.empty()

    else:
        # Static chart if not playing
        current_data = hourly_complete
        static_chart = alt.Chart(current_data).mark_line(
            interpolate='monotone',
            point=True,
            color="green"
        ).encode(
            x=alt.X("hour:O", title="Hour of Day"),
            y=alt.Y("count:Q", title="Songs Played"),
            tooltip=["hour", "count"]
        ).properties(title="🎥 Songs Played by Hour")
        placeholder.altair_chart(static_chart, use_container_width=True)


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

        # --- Most Active Month Listening Insights ---
    st.subheader("📅 Highlights from Most Active Month")

    # Find the most active month
    spotify_df["year_month"] = spotify_df["datetime"].dt.to_period("M")
    monthly_activity = spotify_df.groupby("year_month").size().reset_index(name="plays")
    most_active_month = monthly_activity.sort_values("plays", ascending=False).iloc[0]["year_month"]

    # Filter data for that month
    active_month_df = spotify_df[spotify_df["year_month"] == most_active_month]

    st.markdown(f"### 📈 Top in {most_active_month.strftime('%B %Y')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🎤 Top 5 Artists")
        top5_artists_month = active_month_df.groupby("artistName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        artist_month_chart = alt.Chart(top5_artists_month).mark_bar(color="limegreen").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("artistName:N", sort='-x', title="Artist"),
            tooltip=["artistName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(artist_month_chart, use_container_width=True)

    with col2:
        st.write("🎵 Top 5 Songs")
        top5_songs_month = active_month_df.groupby("trackName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        song_month_chart = alt.Chart(top5_songs_month).mark_bar(color="skyblue").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("trackName:N", sort='-x', title="Song"),
            tooltip=["trackName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(song_month_chart, use_container_width=True)

    with col3:
        st.write("🎼 Top 5 Genres")
        if "main_genre" in active_month_df.columns:
            top5_genres_month = active_month_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            genre_month_chart = alt.Chart(top5_genres_month).mark_bar(color="violet").encode(
                x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                y=alt.Y("main_genre:N", sort='-x', title="Genre"),
                tooltip=["main_genre", "msPlayed"]
            ).properties(height=300)
            st.altair_chart(genre_month_chart, use_container_width=True)
        else:
            st.info("No genre data available for the most active month.")


    # --- Weekly Listening Trend ---
    st.subheader("🌅 Weekly Listening Trend")
    weekly_df = spotify_df.copy()
    weekly_df["week"] = weekly_df["datetime"].dt.isocalendar().week
    week_trend = weekly_df.groupby("week").size().reset_index(name="count")

    week_chart = alt.Chart(week_trend).mark_line(point=True, interpolate='monotone', color="green").encode(
        x=alt.X("week:O", title="Week of the Year"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["week", "count"]
    ).properties(title="Weekly Songs Played")
    st.altair_chart(week_chart, use_container_width=True)

        # --- Weekly Top 5 Highlights ---
    st.subheader("🔥 Top 5 Artists, Songs, and Genres for Most Active Week")

    # Find the most active week
    weekly_df = spotify_df.copy()
    weekly_df["week"] = weekly_df["datetime"].dt.isocalendar().week
    weekly_df["year"] = weekly_df["datetime"].dt.isocalendar().year
    weekly_activity = weekly_df.groupby(["year", "week"]).size().reset_index(name="plays")
    most_active_week = weekly_activity.sort_values("plays", ascending=False).iloc[0]

    # Filter data for that week
    active_week_df = weekly_df[
        (weekly_df["week"] == most_active_week["week"]) &
        (weekly_df["year"] == most_active_week["year"])
    ]

    st.markdown(f"### 🎯 Week {int(most_active_week['week'])} of {int(most_active_week['year'])}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🎤 Top 5 Artists")
        top5_artists_week = active_week_df.groupby("artistName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        artist_week_chart = alt.Chart(top5_artists_week).mark_bar(color="limegreen").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("artistName:N", sort='-x', title="Artist"),
            tooltip=["artistName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(artist_week_chart, use_container_width=True)

    with col2:
        st.write("🎵 Top 5 Songs")
        top5_songs_week = active_week_df.groupby("trackName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        song_week_chart = alt.Chart(top5_songs_week).mark_bar(color="skyblue").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("trackName:N", sort='-x', title="Song"),
            tooltip=["trackName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(song_week_chart, use_container_width=True)

    with col3:
        st.write("🎼 Top 5 Genres")
        if "main_genre" in active_week_df.columns:
            top5_genres_week = active_week_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            genre_week_chart = alt.Chart(top5_genres_week).mark_bar(color="violet").encode(
                x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                y=alt.Y("main_genre:N", sort='-x', title="Genre"),
                tooltip=["main_genre", "msPlayed"]
            ).properties(height=300)
            st.altair_chart(genre_week_chart, use_container_width=True)
        else:
            st.info("No genre data available for the most active week.")
            
        # --- Most Listened Day Highlights ---
    st.subheader("📅 Highlights from Most Listened Day")

    # Find the most listened day
    most_listened_day = spotify_df.groupby("date").size().sort_values(ascending=False).idxmax()
    most_listened_day_df = spotify_df[spotify_df["date"] == most_listened_day]

    st.markdown(f"### 🗓️ {pd.to_datetime(most_listened_day).strftime('%A, %B %d, %Y')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🎤 Top 5 Artists")
        top5_artists_day = most_listened_day_df.groupby("artistName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        artists_day_chart = alt.Chart(top5_artists_day).mark_bar(color="limegreen").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("artistName:N", sort='-x', title="Artist"),
            tooltip=["artistName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(artists_day_chart, use_container_width=True)

    with col2:
        st.write("🎵 Top 5 Songs")
        top5_songs_day = most_listened_day_df.groupby("trackName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
        songs_day_chart = alt.Chart(top5_songs_day).mark_bar(color="skyblue").encode(
            x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
            y=alt.Y("trackName:N", sort='-x', title="Song"),
            tooltip=["trackName", "msPlayed"]
        ).properties(height=300)
        st.altair_chart(songs_day_chart, use_container_width=True)

    with col3:
        st.write("🎼 Top 5 Genres")
        if "main_genre" in most_listened_day_df.columns:
            top5_genres_day = most_listened_day_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            genres_day_chart = alt.Chart(top5_genres_day).mark_bar(color="violet").encode(
                x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                y=alt.Y("main_genre:N", sort='-x', title="Genre"),
                tooltip=["main_genre", "msPlayed"]
            ).properties(height=300)
            st.altair_chart(genres_day_chart, use_container_width=True)
        else:
            st.info("No genre data available for this day.")
    

    # --- Hourly Listening Trend for Most Listened Day ---
    st.subheader("⏰ Hourly Listening Trend for Most Listened Day")

    hourly_most_day_df = most_listened_day_df.copy()
    hourly_most_day_df["hour"] = hourly_most_day_df["datetime"].dt.hour
    hourly_counts_most_day = hourly_most_day_df.groupby("hour")["msPlayed"].count().reset_index().rename(columns={"msPlayed": "count"})

    # Fill missing hours
    full_hours = pd.DataFrame({"hour": list(range(24))})
    hourly_counts_most_day = pd.merge(full_hours, hourly_counts_most_day, on="hour", how="left").fillna(0)

    hourly_chart_most_day = alt.Chart(hourly_counts_most_day).mark_line(
        point=True, interpolate='monotone', color="green"
    ).encode(
        x=alt.X("hour:O", title="Hour of Day"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["hour", "count"]
    ).properties(title="Hourly Songs Played on Most Listened Day")

    st.altair_chart(hourly_chart_most_day, use_container_width=True)


    # --- Top 10 Artists (All Time) ---
    st.subheader("🎶 Top 10 Most Popular Artists (All Time)")
    top10_artists = spotify_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(10).reset_index()

    top10_chart = alt.Chart(top10_artists).mark_bar(color="green").encode(
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

    # --- Seasonal Listening Highlights ---
    st.subheader("🍂 Seasonal Listening Highlights")

    seasons = ["❄️ Winter", "🌸 Spring", "☀️ Summer", "🍂 Autumn"]

    for season in seasons:
        st.markdown(f"### {season}")

        season_df = spotify_df[spotify_df["season"] == season]

        if season_df.empty:
            st.warning(f"No data available for {season}!")
            continue

        col1, col2, col3 = st.columns(3)

        # Top 5 Songs
        with col1:
            st.write(f"🎵 Top 5 Songs")
            if "trackName" in season_df.columns:
                top_songs = season_df.groupby("trackName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
                top_songs["minutes"] = top_songs["msPlayed"] / (1000 * 60)

                song_chart = alt.Chart(top_songs).mark_bar(color="blue").encode(
                    x=alt.X("minutes:Q", title="Minutes Played"),
                    y=alt.Y("trackName:N", sort='-x', title="Song"),
                    tooltip=["trackName", "minutes"]
                ).properties(height=300)
                st.altair_chart(song_chart, use_container_width=True)

        # Top 5 Artists
        with col2:
            st.write(f"👨‍🎤 Top 5 Artists")
            top_artists = season_df.groupby("artistName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            top_artists["minutes"] = top_artists["msPlayed"] / (1000 * 60)

            artist_chart = alt.Chart(top_artists).mark_bar(color="green").encode(
                x=alt.X("minutes:Q", title="Minutes Played"),
                y=alt.Y("artistName:N", sort='-x', title="Artist"),
                tooltip=["artistName", "minutes"]
            ).properties(height=300)
            st.altair_chart(artist_chart, use_container_width=True)

        # Top 5 Genres
        with col3:
            st.write(f"🎼 Top 5 Genres")
            if "main_genre" in season_df.columns:
                top_genres = season_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
                top_genres["minutes"] = top_genres["msPlayed"] / (1000 * 60)

                genre_chart = alt.Chart(top_genres).mark_bar(color="purple").encode(
                    x=alt.X("minutes:Q", title="Minutes Played"),
                    y=alt.Y("main_genre:N", sort='-x', title="Genre"),
                    tooltip=["main_genre", "minutes"]
                ).properties(height=300)
                st.altair_chart(genre_chart, use_container_width=True)

# --- Main Run ---
if __name__ == "__main__":
    spotify_df = load_spotify_data()
    show_spotify_dashboard(spotify_df)
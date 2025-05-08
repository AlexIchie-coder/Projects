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
            .shine-subheader {
                font-size: 28px;
                color: #00cc66;
                text-shadow: 1px 1px 5px #00cc66, 1px 1px 8px #00994d;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            div.stButton > button {
                background-color: #1DB954;
                color: green;
                border-radius: 10px;
                height: 50px;
                font-size: 20px;
            }
            @keyframes glowSpotify {
              0% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff, 0 0 20px #0072ff; }
              50% { text-shadow: 0 0 20px #ff6ec4, 0 0 30px #ff6ec4, 0 0 40px #ff6ec4; }
              100% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff, 0 0 20px #0072ff; }
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

    st.markdown(f"<div class='shine-subheader'>🎼 Listening Summary for {pd.to_datetime(selected_date).strftime('%A, %B %d')}</div>", unsafe_allow_html=True)
    st.metric("Total Songs Played", len(daily_df))

    # --- Top 5 Artists ---
    st.markdown('<div class="shine-subheader">Top 5 Artists</div>', unsafe_allow_html=True)
    top_artists = daily_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(5).reset_index()
    artists_chart = alt.Chart(top_artists).mark_bar(color="green").encode(
        x=alt.X("artistName:N", title="Artist", sort='-y'),
        y=alt.Y("msPlayed:Q", title="Songs Played"),
        tooltip=["artistName", "msPlayed"]
    ).properties(title="Top 5 Artists")
    st.altair_chart(artists_chart, use_container_width=True)

    # --- Top 5 Genres ---
    st.markdown('<div class="shine-subheader">Top 5 Genres</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="shine-subheader">Hourly Listening Trend</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="shine-subheader">🕰️ Hourly Listening Radial Clock</div>', unsafe_allow_html=True)
    radial_chart = alt.Chart(hourly_complete).mark_arc(innerRadius=50, outerRadius=150).encode(
        theta=alt.Theta("count:Q", stack=True),
        color=alt.Color("hour:O", scale=alt.Scale(scheme="greens")),
        tooltip=["hour", "count"]
    ).properties(title="Songs Played by Hour (Radial View)")
    st.altair_chart(radial_chart, use_container_width=True)

    # --- Monthly Listening Trends ---
    st.markdown('<div class="shine-subheader">Monthly Listening Trends</div>', unsafe_allow_html=True)
    monthly_df = spotify_df.groupby(["year", "month"]).size().reset_index(name="count")
    monthly_df["date"] = pd.to_datetime(monthly_df[["year", "month"]].assign(day=1))

    monthly_chart = alt.Chart(monthly_df).mark_area(color="green", interpolate="monotone").encode(
        x=alt.X("date:T", title="Month"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["year", "month", "count"]
    ).properties(title="Monthly Listening Trends")
    st.altair_chart(monthly_chart, use_container_width=True)


    # --- Weekly Listening Trend ---
    st.markdown('<div class="shine-subheader">🌅 Weekly Listening Trends</div>', unsafe_allow_html=True)
    weekly_df = spotify_df.copy()
    weekly_df["week"] = weekly_df["datetime"].dt.isocalendar().week
    week_trend = weekly_df.groupby("week").size().reset_index(name="count")

    week_chart = alt.Chart(week_trend).mark_line(
        point=True, interpolate='monotone', color="green"
    ).encode(
        x=alt.X("week:O", title="Week of the Year"),
        y=alt.Y("count:Q", title="Songs Played"),
        tooltip=["week", "count"]
    ).properties(title="Weekly Songs Played")
    st.altair_chart(week_chart, use_container_width=True)

    # --- Weekly, Monthly, and Daily Highlights Section ---
    with st.expander("🔥 Top 5 Artists, Songs, and Genres for Most Active Week", expanded=True):
        # Find the most active week
        weekly_df["year"] = weekly_df["datetime"].dt.isocalendar().year
        weekly_activity = weekly_df.groupby(["year", "week"]).size().reset_index(name="plays")
        most_active_week = weekly_activity.sort_values("plays", ascending=False).iloc[0]

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

    with st.expander("📅 Highlights from Most Active Month", expanded=False):
        # Find the most active month
        monthly_df = spotify_df.copy()
        monthly_df["month"] = monthly_df["datetime"].dt.month
        monthly_df["year"] = monthly_df["datetime"].dt.year
        monthly_activity = monthly_df.groupby(["year", "month"]).size().reset_index(name="plays")
        most_active_month = monthly_activity.sort_values("plays", ascending=False).iloc[0]

        active_month_df = monthly_df[
            (monthly_df["month"] == most_active_month["month"]) &
            (monthly_df["year"] == most_active_month["year"])
        ]

        month_name = pd.to_datetime(f"{int(most_active_month['year'])}-{int(most_active_month['month'])}-01").strftime('%B')

        st.markdown(f"### 📈 Top in {month_name} {int(most_active_month['year'])}")

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

    with st.expander("📅 Highlights from Most Listened Day", expanded=False):
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
    st.markdown('<div class="shine-subheader">⏰ Hourly Listening Trend for Most Listened Day</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="shine-subheader">🎶 Top 10 Most Popular Artists (All Time)</div>', unsafe_allow_html=True)
    top10_artists = spotify_df.groupby("artistName")["msPlayed"].count().sort_values(ascending=False).head(10).reset_index()

    top10_chart = alt.Chart(top10_artists).mark_bar(color="green").encode(
        x=alt.X("msPlayed:Q", title="Total Listening (ms)"),
        y=alt.Y("artistName:N", sort='-x', title="Artist"),
        tooltip=["artistName", "msPlayed"]
    ).properties(title="Top 10 Most Popular Artists (All Time)")
    st.altair_chart(top10_chart, use_container_width=True)

    # --- Pie Chart: Listening by Season ---
    st.markdown('<div class="shine-subheader">🌎 Overall Listening by Season</div>', unsafe_allow_html=True)
    season_summary = spotify_df.groupby("season")["msPlayed"].sum().reset_index()
    season_summary["percent"] = (season_summary["msPlayed"] / season_summary["msPlayed"].sum()) * 100

    pie_chart = alt.Chart(season_summary).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="msPlayed", type="quantitative"),
        color=alt.Color(field="season", type="nominal"),
        tooltip=[alt.Tooltip("season:N"), alt.Tooltip("percent:Q", format=".2f")]
    ).properties(title="Season Share of Total Listening")
    st.altair_chart(pie_chart, use_container_width=True)

    # --- Seasonal Listening Highlights ---
        # --- Seasonal Listening Highlights ---
    st.markdown('<div class="shine-subheader">🍂 Seasonal Listening Highlights</div>', unsafe_allow_html=True)

    season_options = ["❄️ Winter", "🌸 Spring", "☀️ Summer", "🍂 Autumn"]
    selected_season = st.selectbox("Select a Season to Explore", season_options)

    season_df = spotify_df[spotify_df["season"] == selected_season]

    if season_df.empty:
        st.warning(f"No listening data available for {selected_season}.")
    else:
        st.markdown(f"### 📊 {selected_season} Highlights")

        col1, col2, col3 = st.columns(3)

        # Top 5 Songs
        with col1:
            st.write("🎵 Top 5 Songs")
            top5_songs_season = season_df.groupby("trackName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            songs_season_chart = alt.Chart(top5_songs_season).mark_bar(color="skyblue").encode(
                x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                y=alt.Y("trackName:N", sort='-x', title="Song"),
                tooltip=["trackName", "msPlayed"]
            ).properties(height=300)
            st.altair_chart(songs_season_chart, use_container_width=True)

        # Top 5 Artists
        with col2:
            st.write("👨‍🎤 Top 5 Artists")
            top5_artists_season = season_df.groupby("artistName")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
            artists_season_chart = alt.Chart(top5_artists_season).mark_bar(color="limegreen").encode(
                x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                y=alt.Y("artistName:N", sort='-x', title="Artist"),
                tooltip=["artistName", "msPlayed"]
            ).properties(height=300)
            st.altair_chart(artists_season_chart, use_container_width=True)

        # Top 5 Genres
        with col3:
            st.write("🎼 Top 5 Genres")
            if "main_genre" in season_df.columns:
                top5_genres_season = season_df.groupby("main_genre")["msPlayed"].sum().sort_values(ascending=False).head(5).reset_index()
                genres_season_chart = alt.Chart(top5_genres_season).mark_bar(color="violet").encode(
                    x=alt.X("msPlayed:Q", title="Listening Time (ms)"),
                    y=alt.Y("main_genre:N", sort='-x', title="Genre"),
                    tooltip=["main_genre", "msPlayed"]
                ).properties(height=300)
                st.altair_chart(genres_season_chart, use_container_width=True)
            else:
                st.info("No genre data available for this season.")

# --- Main Run ---
if __name__ == "__main__":
    spotify_df = load_spotify_data()
    show_spotify_dashboard(spotify_df)
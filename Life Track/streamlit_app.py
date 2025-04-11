import streamlit as st
from datetime import datetime

st.set_page_config(page_title="DailyVibe", layout="centered")

st.title("🎧 DailyVibe – A Day in Data")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Log My Day", "View Past Logs"])

# Page 1: Logging Your Day
if page == "Log My Day":
    st.subheader("📍 Where were you today?")
    location = st.text_input("Location Name", placeholder="e.g. Downtown Toronto")
    duration = st.text_input("How long did you stay?", placeholder="e.g. 2h 30m")

    st.subheader("🎶 Songs you listened to")
    songs = st.text_area("List the songs (comma-separated)", placeholder="e.g. Gravity - John Mayer, Stay - Rihanna")

    st.subheader("🌤️ Weather")
    weather = st.text_input("Describe the weather", placeholder="e.g. Sunny, 23°C")

    st.subheader("😊 How did you feel?")
    mood = st.slider("Mood Rating", 1, 10)

    if st.button("Save Day"):
        st.success("Day logged! (We'll connect DB in the next step!)")

# Page 2: View Logs
else:
    st.subheader("📆 Past Logs")
    st.info("We’ll add the DB view functionality soon!")

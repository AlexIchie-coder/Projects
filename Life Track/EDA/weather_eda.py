import streamlit as st
st.set_page_config(page_title="Weather Dashboard", layout="wide")

import pandas as pd
import altair as alt
import time
from itertools import cycle
from datetime import timedelta

# --- Load Data
def load_weather_data():
    weather_df = pd.read_csv("merged_weather_data.csv")
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
    weather_df["day_of_week"] = weather_df["datetime"].dt.day_name()
    weather_df["date"] = weather_df["datetime"].dt.date
    return weather_df

# --- Weather Dashboard
def show_weather_dashboard(weather_df):
    placeholder = st.empty()

    # Loading animation
    with placeholder.container():
        st.title("🌤️ Loading Your Weather Dashboard...")
        st.progress(30)
        time.sleep(0.8)
        st.progress(60)
        time.sleep(0.6)
        st.progress(100)

    placeholder.empty()
    st.title("🌤️ Weather Dashboard")

    # City selector with unique key
    cities = sorted(weather_df["city"].unique())
    selected_city = st.selectbox("Select a city", cities, key="weather_dashboard_city_selector")
    city_df = weather_df[weather_df["city"] == selected_city]

    today = city_df["datetime"].max().normalize()
    today_data = city_df[city_df["datetime"].dt.date == today.date()]

    if today_data.empty:
        st.warning("No data for today.")
        return

    # Emoji animation
    emoji_cycle = cycle(["☁️", "🌧️", "🌤️", "☀️"])
    emoji_placeholder = st.empty()
    for _ in range(6):
        emoji_placeholder.markdown(f"### Loading condition... {next(emoji_cycle)}")
        time.sleep(0.2)
    emoji_placeholder.empty()

    # Current Season
    st.subheader("Current Season")
    current_season = today_data["season"].iloc[0] if "season" in today_data.columns else "Unknown"
    st.info(f"It's currently **{current_season}** in {selected_city} 🌱")

    # Today's Summary
    st.subheader("Today's Weather Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{today_data['temp'].iloc[0]:.1f} °C")
    col2.metric("Precipitation", f"{today_data['precip'].iloc[0]:.1f} mm")
    col3.metric("Windspeed", f"{today_data['windspeed'].iloc[0]:.1f} km/h")

    # 📊 Visual Summary: Today's Weather vs Avg
    st.subheader("📊 Visual Summary: Today vs Weekly Average")

    past_week = city_df[city_df["datetime"] < today].sort_values("datetime").tail(7)
    avg_temp = past_week["temp"].mean() if not past_week.empty else None
    avg_precip = past_week["precip"].mean() if not past_week.empty else None
    avg_wind = past_week["windspeed"].mean() if not past_week.empty else None

    today_chart_data = pd.DataFrame({
        "Metric": ["🌡️ Temperature", "🌧️ Precipitation", "💨 Windspeed"],
        "Value": [
            today_data["temp"].iloc[0],
            today_data["precip"].iloc[0],
            today_data["windspeed"].iloc[0]
        ],
        "Average": [avg_temp, avg_precip, avg_wind],
        "Color": ["#ff4d4d", "#80bfff", "#66ccff"]
    })

    bar_chart = alt.Chart(today_chart_data).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Value:Q", title="Today's Value"),
        color=alt.Color("Color:N", scale=None),
        tooltip=["Metric", "Value"]
    ).properties(
        height=300,
        title="Today's Weather with 7-Day Avg Reference"
    )

    avg_lines = alt.Chart(today_chart_data).mark_rule(strokeDash=[6, 6], color="orange").encode(
        y="Average:Q",
        tooltip=["Metric", "Average"]
    )

    st.altair_chart(bar_chart + avg_lines, use_container_width=True)

    # 📉 Past Days Temperature
    st.subheader("📉 Past 7 Days Temperature Trend")
    past_data = city_df[city_df["datetime"] < today].sort_values("datetime").tail(7)
    if not past_data.empty:
        chart = alt.Chart(past_data).mark_bar().encode(
            x=alt.X("day_of_week:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
            y=alt.Y("temp:Q", title="Temperature (°C)"),
            color=alt.Color("temp:Q", scale=alt.Scale(scheme="redblue")),
            tooltip=["datetime", "temp"]
        ).properties(title="Last 7 Days Temperature")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Not enough data for past week trend.")

    # 👕 Clothing Tip
    st.subheader("👕 Clothing Recommendation")
    if "clothing_recommendation" in today_data.columns:
        st.success(today_data["clothing_recommendation"].iloc[0])
    else:
        st.info("No clothing tip available.")

    # 🌤️ Final Weather Emoji
    condition = today_data["condition"].iloc[0] if "condition" in today_data.columns else ""
    emoji = "☀️" if "sun" in condition.lower() else "🌧️" if "rain" in condition.lower() else "☁️"
    st.markdown(f"### Today's Condition: {emoji} **{condition}**")

    # 📅 3-Day Forecast
    st.subheader("📅 Next 3 Days Forecast")

    forecast_dates = pd.date_range(today + timedelta(days=1), periods=3).date
    forecast_df = city_df[city_df["date"].isin(forecast_dates)]

    if not forecast_df.empty:
        for date in forecast_dates:
            day_data = forecast_df[forecast_df["date"] == date]
            if not day_data.empty:
                row = day_data.iloc[0]
                emoji = "☀️" if "sun" in row["condition"].lower() else "🌧️" if "rain" in row["condition"].lower() else "☁️"
                st.markdown(f"**{date.strftime('%A, %b %d')}** {emoji}")
                st.write(f"- Temperature: {row['temp']} °C")
                st.write(f"- Precipitation: {row['precip']} mm")
                st.write(f"- Windspeed: {row['windspeed']} km/h")
                st.write(f"- Condition: {row['condition']}")
                st.markdown("---")
    else:
        st.info("No forecast data available for the next 3 days.")

# --- Run Only When This File is Executed Directly ---
if __name__ == "__main__":
    weather_df = load_weather_data()
    show_weather_dashboard(weather_df)

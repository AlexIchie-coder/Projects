import streamlit as st
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
    # --- Add Custom CSS
    st.markdown("""
        <style>
        @keyframes glow {
          0% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff, 0 0 20px #0072ff; }
          50% { text-shadow: 0 0 20px #ff6ec4, 0 0 30px #ff6ec4, 0 0 40px #ff6ec4; }
          100% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff, 0 0 20px #0072ff; }
        }
        .glow-title {
            font-size: 60px;
            color: white;
            text-align: center;
            animation: glow 2s infinite;
            font-weight: bold;
            margin-bottom: 0px;
        }
        .glow-season {
            font-size: 40px;
            color: white;
            text-align: center;
            animation: glow 2s infinite;
            margin-top: -10px;
            font-weight: bold;
        }
        .shiny-subheader {
            font-size: 28px;
            color: #00c6ff;
            text-shadow: 1px 1px 5px #00c6ff, 1px 1px 8px #0072ff;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .big-recommendation {
            font-size: 32px;
            background: linear-gradient(135deg, #e0f7fa, #ffffff);
            padding: 25px 20px;
            border-radius: 18px;
            text-align: center;
            font-weight: bold;
            color: #003366; /* Darker text for better contrast */
            box-shadow: 0 4px 20px rgba(0, 198, 255, 0.4);
            max-width: 800px;
            margin: 20px auto;
            line-height: 1.5;
            }

        }
        </style>
    """, unsafe_allow_html=True)

    placeholder = st.empty()

    with placeholder.container():
        st.markdown('<div class="glow-title">🌤️ Loading Your Weather Dashboard...</div>', unsafe_allow_html=True)
        st.progress(30)
        time.sleep(0.8)
        st.progress(60)
        time.sleep(0.6)
        st.progress(100)

    placeholder.empty()

    # --- Weather Dashboard Title
    st.markdown('<div class="glow-title">🌤️ Weather Dashboard</div>', unsafe_allow_html=True)

    cities = sorted(weather_df["city"].unique())
    selected_city = st.selectbox("Select a city", cities, key="weather_dashboard_city_selector")
    city_df = weather_df[weather_df["city"] == selected_city]

    today = city_df["datetime"].max().normalize()
    today_data = city_df[city_df["datetime"].dt.date == today.date()]

    if today_data.empty:
        st.warning("No data for today.")
        return

    # --- Current Season Glowing
    season_emoji = {
        "Spring": "🌸",
        "Summer": "☀️",
        "Autumn": "🍂",
        "Winter": "❄️"
    }
    current_season = today_data["season"].iloc[0] if "season" in today_data.columns else "Unknown"
    emoji = season_emoji.get(current_season, "🌱")
    st.markdown(f'<div class="glow-season">{emoji} Current Season: {current_season} {emoji}</div>', unsafe_allow_html=True)

    st.write("##")

    emoji_cycle = cycle(["☁️", "🌧️", "🌤️", "☀️"])
    emoji_placeholder = st.empty()
    for _ in range(6):
        emoji_placeholder.markdown(f"### Loading condition... {next(emoji_cycle)}")
        time.sleep(0.2)
    emoji_placeholder.empty()

    # --- Today's Weather Summary
    st.markdown('<div class="shiny-subheader">📋 Today\'s Weather Summary</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    cols[0].metric("🌡️ Temperature", f"{today_data['temp'].iloc[0]:.1f} °C")
    cols[1].metric("🌧️ Precipitation", f"{today_data['precip'].iloc[0]:.1f} mm")
    cols[2].metric("💨 Windspeed", f"{today_data['windspeed'].iloc[0]:.1f} km/h")
    if 'humidity' in today_data.columns:
        cols[3].metric("💧 Humidity", f"{today_data['humidity'].iloc[0]:.0f}%")

    st.write("##")

    # --- Compare Today's Weather with Weekly Average
    st.markdown('<div class="shiny-subheader">📊 Today\'s Weather Compared to Weekly Avg</div>', unsafe_allow_html=True)
    last_week = today - timedelta(days=7)
    last_week_data = city_df[(city_df["datetime"] >= last_week) & (city_df["datetime"] <= today)]

    if not last_week_data.empty:
        avg_temp = last_week_data["temp"].mean()
        avg_precip = last_week_data["precip"].mean()
        avg_wind = last_week_data["windspeed"].mean()

        delta_temp = today_data["temp"].iloc[0] - avg_temp
        delta_precip = today_data["precip"].iloc[0] - avg_precip
        delta_wind = today_data["windspeed"].iloc[0] - avg_wind

        cols = st.columns(3)
        cols[0].metric("🌡️ Temp vs Avg", f"{today_data['temp'].iloc[0]:.1f} °C", f"{delta_temp:+.1f}")
        cols[1].metric("🌧️ Precip vs Avg", f"{today_data['precip'].iloc[0]:.1f} mm", f"{delta_precip:+.1f}")
        cols[2].metric("💨 Wind vs Avg", f"{today_data['windspeed'].iloc[0]:.1f} km/h", f"{delta_wind:+.1f}")

    st.write("---")

    # --- Past 7 Days Temperature Trend
    st.markdown('<div class="shiny-subheader">📈 Past 7 Days Temperature Trend</div>', unsafe_allow_html=True)
    temp_trend = last_week_data.groupby("date")["temp"].mean().reset_index()

    line_chart = alt.Chart(temp_trend).mark_line(point=True, strokeDash=[5,5]).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("temp:Q", title="Avg Temp (°C)"),
        tooltip=["date", "temp"]
    ).properties(
        width=700,
        height=400
    ).interactive()

    st.altair_chart(line_chart)

    st.write("---")

    # --- Extreme Weather Highlights
    st.markdown('<div class="shiny-subheader">⚡ Extreme Weather Highlights</div>', unsafe_allow_html=True)
    col1, col2, col3, col4= st.columns(4)

    top_hottest = city_df.sort_values(by="temp", ascending=False).head(5)
    top_coldest = city_df.sort_values(by="temp", ascending=True).head(5)
    top_rainiest = city_df.sort_values(by="precip", ascending=False).head(5)

    with col1:
        st.markdown("#### 🔥 Top 5 Hottest Days")
        for idx, row in top_hottest.iterrows():
            st.write(f"{row['date']} - {row['temp']:.1f} °C")
    with col2:
        st.markdown("#### ❄️ Top 5 Coldest Days")
        for idx, row in top_coldest.iterrows():
            st.write(f"{row['date']} - {row['temp']:.1f} °C")
    with col3:
        st.markdown("#### 🌧️ Top 5 Rainiest Days")
        for idx, row in top_rainiest.iterrows():
            st.write(f"{row['date']} - {row['precip']:.1f} mm")

    st.write("---")

    # --- Clothing Recommendation (from your dataset)
    st.markdown('<div class="shiny-subheader">🧥 Today\'s Clothing Recommendation</div>', unsafe_allow_html=True)
    if 'clothing_recommendation' in today_data.columns:
        recommendation = today_data['clothing_recommendation'].iloc[0]
    else:
        recommendation = "No recommendation available."

    st.markdown(f'<div class="big-recommendation">{recommendation}</div>', unsafe_allow_html=True)

    
    # --- Past 7 Days Temperature Trend
    st.subheader("📉 Past 7 Days Temperature Trend")
    past_data = city_df[city_df["datetime"] < today].sort_values("datetime").tail(7)
    if not past_data.empty:
        chart = alt.Chart(past_data).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8,
            interpolate='monotone'
        ).encode(
            x=alt.X("day_of_week:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
            y=alt.Y("temp:Q", title="Temperature (°C)"),
            color=alt.Color("temp:Q", scale=alt.Scale(scheme="redblue")),
            tooltip=["datetime", "temp"]
        ).properties(title="Last 7 Days Temperature")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Not enough data for past week trend.")

    # --- Seasonal Insights
    st.header("🌸☀️🍂❄️ Seasonal Insights")

    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    for season in seasons:
        emoji = season_emoji.get(season, "🌱")
        st.subheader(f"Season: {season} {emoji}")
        season_df = city_df[city_df["season"] == season]

        if season_df.empty:
            st.info(f"No data for {season}.")
            continue

        avg_temp = season_df["temp"].mean()
        avg_precip = season_df["precip"].mean()
        avg_wind = season_df["windspeed"].mean()

        weather_chart_data = pd.DataFrame({
            "Metric": ["Temperature (°C)", "Precipitation (mm)", "Windspeed (km/h)"],
            "Average": [avg_temp, avg_precip, avg_wind],
            "Color": ["#ff4d4d", "#80bfff", "#66ccff"]
        })

        bars = alt.Chart(weather_chart_data).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8
        ).encode(
            x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Average:Q", title="Average Value"),
            color=alt.Color("Color:N", scale=None),
            tooltip=["Metric", "Average"]
        )

        st.altair_chart(bars, use_container_width=True)

        if "clothing_recommendation" in season_df.columns:
            clothing_counts = season_df["clothing_recommendation"].value_counts().head(5).reset_index()
            clothing_counts.columns = ["Clothing", "Count"]

            pie = alt.Chart(clothing_counts).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Clothing", type="nominal", scale=alt.Scale(scheme="pastel2")),
                tooltip=["Clothing", "Count"]
            ).properties(
                title=f"🧥 Top 5 Clothing Recommendations - {season}"
            )

            st.altair_chart(pie, use_container_width=True)
        else:
            st.info(f"No clothing recommendation data for {season}.")

    # --- Full Year Summary
    st.header("📈 Weather Summary - Full Year")
    full_year_chart = alt.Chart(city_df).mark_line(
        interpolate='monotone',
        point=True
    ).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('temp:Q', title='Temperature (°C)'),
        tooltip=['date', 'temp']
    ).properties(
        title="🌡️ Daily Temperature Throughout the Year",
        height=400
    )
    st.altair_chart(full_year_chart, use_container_width=True)

    # --- Clothing Recommendation Full Year
    st.header("🧥 Clothing Recommendation - Full Year")
    if "clothing_recommendation" in city_df.columns:
        full_year_clothing = city_df["clothing_recommendation"].value_counts().reset_index()
        full_year_clothing.columns = ["Clothing", "Count"]

        full_year_pie = alt.Chart(full_year_clothing).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Clothing", type="nominal", scale=alt.Scale(scheme="set3")),
            tooltip=["Clothing", "Count"]
        ).properties(
            title="👗 Clothing Recommendations Across the Year"
        )
        st.altair_chart(full_year_pie, use_container_width=True)
    else:
        st.info("No clothing recommendation data for full year.")

    # --- Today's Condition
    condition = today_data["condition"].iloc[0] if "condition" in today_data.columns else ""
    condition_lower = condition.lower()
    if "sun" in condition_lower:
        emoji = "☀️"
    elif "rain" in condition_lower:
        emoji = "🌧️"
    elif "snow" in condition_lower:
        emoji = "❄️"
    else:
        emoji = "☁️"

    st.markdown(f"### Today's Condition: {emoji} **{condition}**")

    # --- Next 3 Days Forecast
    st.subheader("📅 Next 3 Days Forecast")
    forecast_dates = pd.date_range(today + timedelta(days=1), periods=3).date
    forecast_df = city_df[city_df["date"].isin(forecast_dates)]

    if not forecast_df.empty:
        for date in forecast_dates:
            day_data = forecast_df[forecast_df["date"] == date]
            if not day_data.empty:
                row = day_data.iloc[0]
                condition_lower = row["condition"].lower()
                if "sun" in condition_lower:
                    emoji = "☀️"
                elif "rain" in condition_lower:
                    emoji = "🌧️"
                elif "snow" in condition_lower:
                    emoji = "❄️"
                else:
                    emoji = "☁️"

                st.markdown(f"**{date.strftime('%A, %b %d')}** {emoji}")
                st.write(f"- Temperature: {row['temp']} °C")
                st.write(f"- Precipitation: {row['precip']} mm")
                st.write(f"- Windspeed: {row['windspeed']} km/h")
                if "humidity" in row:
                    st.write(f"- Humidity: {row['humidity']}%")
                st.write(f"- Condition: {row['condition']}")
                st.markdown("---")
    else:
        st.info("No forecast data available for the next 3 days.")

# --- Run App
if __name__ == "__main__":
    weather_df = load_weather_data()
    show_weather_dashboard(weather_df)

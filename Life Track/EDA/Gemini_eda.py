# %% [markdown]
# # GEMINI AI API

# %%
import sys
print(sys.path)

# %%
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access your API key
GEMINI_API = os.getenv("Gemini_API")

#print(GEMINI_API)  # Just to confirm it's loading correctly


# %% [markdown]
# # Summarizing my Weather and Spotify API with GeminiAI API

# %% [markdown]
# # Summer Dairy Summary

# %%
# 🎵 Spotify Summary - Top 3 Genres by Listening Time in Summer
spotify_summary = spotify_df[spotify_df['season'] == 'Summer'] \
    .groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

# Convert msPlayed to minutes for display
spotify_summary_minutes = (spotify_summary / 60000).round(2)
print("🎧 Top 3 Most Listened Genres in Summer (by Minutes):")
print(spotify_summary_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in Summer
top_artists_summer = spotify_df[spotify_df['season'] == 'Summer'] \
    .groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_artists_minutes = (top_artists_summer / 60000).round(2)

print("🎤 Top 3 Most Listened Artists in Summer:")
print(top_artists_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in Summer
top_songs_summer = spotify_df[spotify_df['season'] == 'Summer'] \
    .groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_songs_minutes = (top_songs_summer / 60000).round(2)

print("🎶 Top 3 Most Listened Songs in Summer:")
print(top_songs_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed in Summer for Berlin only
weather_summary = weather_df[
    (weather_df['season'] == 'Summer') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print("🌞 Average Summer Weather in Berlin:")
print(weather_summary.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation (from dataset) - Summer in Berlin
clothing_recs = weather_df[
    (weather_df['season'] == 'Summer') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
]['clothing_recommendation'].dropna().unique()

print("\n🧥 Clothing Recommendation for Berlin in Summer:")
for rec in clothing_recs:
    print(f"- {rec}")



# %%
summary_text = f"""
🎧 **Top Music Genres in Summer** (by msPlayed):
{spotify_summary.to_string()}

🎤 **Top 3 Artists in Summer**:
{top_artists_summer.to_string()}

🎶 **Top 3 Songs in Summer**:
{top_songs_summer.to_string()}

🌞 **Average Summer Weather in Berlin**:
{weather_summary.to_string(float_format='%.1f')}
"""

print(summary_text)


# %%
import os
import pandas as pd
from datetime import datetime
from google import generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

GEMINI_API = os.getenv("Gemini_API")


genai.configure(api_key=GEMINI_API)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"""
Write a personal summer diary entry based on this data:

🎧 Top Genres in Summer:
{spotify_summary.to_string()}

🎤 Top 3 Artists in Summer:
{top_artists_summer.to_string()}

🎶 Top 3 Songs in Summer:
{top_songs_summer.to_string()}

🌞 Weather Summary (Berlin):
{weather_summary.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Summer in Berlin:
{clothing_recs}

Make it casual, reflective, and maybe a bit poetic!
"""

response = model.generate_content(prompt)

print(response.text)


# %% [markdown]
# ## Autumn Dairy Summery

# %%
# 🎵 Spotify Summary - Top 3 Genres by Listening Time in Autumn
spotify_autumn = spotify_df[spotify_df['season'] == 'Autumn'] \
    .groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

# Convert msPlayed to minutes for display
spotify_autumn_minutes = (spotify_autumn / 60000).round(2)
print("🎧 Top 3 Most Listened Genres in Autumn (by Minutes):")
print(spotify_autumn_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in Autumn
top_artists_autumn = spotify_df[spotify_df['season'] == 'Autumn'] \
    .groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_artists_autumn_minutes = (top_artists_autumn / 60000).round(2)

print("🎤 Top 3 Most Listened Artists in Autumn:")
print(top_artists_autumn_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in Autumn
top_songs_autumn = spotify_df[spotify_df['season'] == 'Autumn'] \
    .groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_songs_autumn_minutes = (top_songs_autumn / 60000).round(2)

print("🎶 Top 3 Most Listened Songs in Autumn:")
print(top_songs_autumn_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed in Autumn for Berlin only
weather_summary_autumn = weather_df[
    (weather_df['season'] == 'Autumn') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print("🌦️ Average Autumn Weather in Berlin:")
print(weather_summary_autumn.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation (from dataset) - Summer in Berlin
clothing_Autumn = weather_df[
    (weather_df['season'] == 'Autumn') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
]['clothing_recommendation'].dropna().unique()

print("\n🧥 Clothing Recommendation for Berlin in Autumn:")
for rec in clothing_Autumn:
    print(f"- {rec}")


# %%
summary_Autumn = f"""
🎧 **Top Music Genres in Autumn** (by Minutes):
{spotify_autumn_minutes.to_string()}

🎤 **Top 3 Artists in Autumn**:
{top_artists_autumn_minutes.to_string()}

🎶 **Top 3 Songs in Autumn**:
{top_songs_autumn_minutes.to_string()}

🌦️ **Average Autumn Weather in Berlin**:
{weather_summary_autumn.to_string(float_format='%.1f')}

"""

print(summary_text)


# %%
#AUTUMN GEMINI API

import google.generativeai as genai

# Make sure GEMINI_API is defined
genai.configure(api_key=GEMINI_API)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create the Autumn prompt
prompt = f"""
Write a personal autumn diary entry based on this data:

🎧 Top Genres in Autumn:
{spotify_autumn_minutes.to_string()}

🎤 Top 3 Artists in Autumn:
{top_artists_autumn_minutes.to_string()}

🎶 Top 3 Songs in Autumn:
{top_songs_autumn_minutes.to_string()}

🌦️ Weather Summary (Berlin):
{weather_summary_autumn.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Autumn in Berlin:
{clothing_Autumn}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate response from Gemini
response = model.generate_content(prompt)

# Display diary entry
print(response.text)


# %% [markdown]
# ## Winter Dairy Summery 

# %%
# 🎵 Spotify Summary - Top 3 Genres by Listening Time in Winter
spotify_winter = spotify_df[spotify_df['season'] == 'Winter'] \
    .groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

# Convert msPlayed to minutes for display
spotify_winter_minutes = (spotify_winter / 60000).round(2)
print("🎧 Top 3 Most Listened Genres in Winter (by Minutes):")
print(spotify_winter_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in Winter
top_artists_winter = spotify_df[spotify_df['season'] == 'Winter'] \
    .groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_artists_winter_minutes = (top_artists_winter / 60000).round(2)

print("🎤 Top 3 Most Listened Artists in Winter:")
print(top_artists_winter_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in Winter
top_songs_winter = spotify_df[spotify_df['season'] == 'Winter'] \
    .groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_songs_winter_minutes = (top_songs_winter / 60000).round(2)

print("🎶 Top 3 Most Listened Songs in Winter:")
print(top_songs_winter_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed in Winter for Berlin only
weather_summary_winter = weather_df[
    (weather_df['season'] == 'Winter') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print("🌨️ Average Winter Weather in Berlin:")
print(weather_summary_winter.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation (from dataset) - Summer in Berlin
clothing_winter = weather_df[
    (weather_df['season'] == 'Winter') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
]['clothing_recommendation'].dropna().unique()

print("\n🧥 Clothing Recommendation for Berlin in Winter:")
for clothing in clothing_winter:
    print(f"- {clothing}")


# %%
summary_Winter = f"""
🎧 **Top Music Genres in Winter** (by Minutes):
{spotify_winter_minutes.to_string()}

🎤 **Top 3 Artists in Winter**:
{top_artists_winter_minutes.to_string()}

🎶 **Top 3 Songs in Winter**:
{top_songs_winter_minutes.to_string()}

🌨️ **Average Winter Weather in Berlin**:
{weather_summary_winter.to_string(float_format='%.1f')}
"""

print(summary_Winter)


# %%
# WINTER GEMINI API

import google.generativeai as genai

# Make sure GEMINI_API is defined
genai.configure(api_key=GEMINI_API)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create the Winter prompt
prompt = f"""
Write a personal winter diary entry based on this data:

🎧 Top Genres in Winter:
{spotify_winter_minutes.to_string()}

🎤 Top 3 Artists in Winter:
{top_artists_winter_minutes.to_string()}

🎶 Top 3 Songs in Winter:
{top_songs_winter_minutes.to_string()}

🌨️ Weather Summary (Berlin):
{weather_summary_winter.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Winter in Berlin:
{clothing_winter}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate response from Gemini
response = model.generate_content(prompt)

# Display diary entry
print(response.text)


# %% [markdown]
# ## Spring Dairy Summery

# %%
# 🎵 Spotify Summary - Top 3 Genres by Listening Time in Spring
spotify_spring = spotify_df[spotify_df['season'] == 'Spring'] \
    .groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

# Convert msPlayed to minutes for display
spotify_spring_minutes = (spotify_spring / 60000).round(2)
print("🎧 Top 3 Most Listened Genres in Spring (by Minutes):")
print(spotify_spring_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in Spring
top_artists_spring = spotify_df[spotify_df['season'] == 'Spring'] \
    .groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_artists_spring_minutes = (top_artists_spring / 60000).round(2)

print("🎤 Top 3 Most Listened Artists in Spring:")
print(top_artists_spring_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in Spring
top_songs_spring = spotify_df[spotify_df['season'] == 'Spring'] \
    .groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)
top_songs_spring_minutes = (top_songs_spring / 60000).round(2)

print("🎶 Top 3 Most Listened Songs in Spring:")
print(top_songs_spring_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed in Spring for Berlin only
weather_summary_spring = weather_df[
    (weather_df['season'] == 'Spring') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print("🌸 Average Spring Weather in Berlin:")
print(weather_summary_spring.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation (from dataset) - Summer in Berlin
clothing_spring = weather_df[
    (weather_df['season'] == 'Spring') &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
]['clothing_recommendation'].dropna().unique()

print("\n🧥 Clothing Recommendation for Berlin in Winter:")
for clothing in clothing_spring:
    print(f"- {clothing}")


# %%
summary_Spring = f"""
🎧 **Top Music Genres in Spring** (by Minutes):
{spotify_spring_minutes.to_string()}

🎤 **Top 3 Artists in Spring**:
{top_artists_spring_minutes.to_string()}

🎶 **Top 3 Songs in Spring**:
{top_songs_spring_minutes.to_string()}

🌸 **Average Spring Weather in Berlin**:
{weather_summary_spring.to_string(float_format='%.1f')}
"""

print(summary_Spring)


# %%
# SPRING GEMINI API

import google.generativeai as genai

# Make sure GEMINI_API is defined
genai.configure(api_key=GEMINI_API)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create the Spring prompt
prompt = f"""
Write a personal spring diary entry based on this data:

🎧 Top Genres in Spring:
{spotify_spring_minutes.to_string()}

🎤 Top 3 Artists in Spring:
{top_artists_spring_minutes.to_string()}

🎶 Top 3 Songs in Spring:
{top_songs_spring_minutes.to_string()}

🌸 Weather Summary (Berlin):
{weather_summary_spring.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Spring in Berlin:
{clothing_spring}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate response from Gemini
response = model.generate_content(prompt)

# Display diary entry
print(response.text)


# %% [markdown]
# ## YEAR Diary Summery

# %%
# 🎵 Spotify Summary - Top 3 Genres by Listening Time in the Year
spotify_year = spotify_df.groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

spotify_year_minutes = (spotify_year / 60000).round(2)
print("🎧 Top 3 Most Listened Genres in the Year (by Minutes):")
print(spotify_year_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in the Year
top_artists_year = spotify_df.groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

top_artists_year_minutes = (top_artists_year / 60000).round(2)
print("🎤 Top 3 Most Listened Artists in the Year:")
print(top_artists_year_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in the Year
top_songs_year = spotify_df.groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

top_songs_year_minutes = (top_songs_year / 60000).round(2)
print("🎶 Top 3 Most Listened Songs in the Year:")
print(top_songs_year_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌍 Weather Summary - Avg Temp, Precip, Windspeed for Berlin (All Year)
weather_summary_year = weather_df[
    weather_df['city'].str.lower().str.strip() == 'berlin'
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print("🌦️ Average Yearly Weather in Berlin:")
print(weather_summary_year.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation - Full Year in Berlin
clothing_year = weather_df[
    weather_df['city'].str.lower().str.strip() == 'berlin'
]['clothing_recommendation'].dropna().unique()

print("👕 Clothing Recommendations for the Year in Berlin:")
for rec in clothing_year:
    print(f"- {rec}")



# %%
summary_year = f"""
🎧 **Top Music Genres in Year** (by Minutes):
{(spotify_year_minutes.to_string())}

🎤 **Top 3 Artists in Year**:
{top_artists_year_minutes.to_string()}

🎶 **Top 3 Songs in Year**:
{top_songs_year_minutes.to_string()}

 **Average Year Weather in Berlin**:
{weather_summary_year.to_string(float_format='%.1f')}
"""

print(summary_year)


# %%
# YEAR GEMINI API

import google.generativeai as genai

# Make sure GEMINI_API is defined
genai.configure(api_key=GEMINI_API)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create the Spring prompt
prompt = f"""
Write a personal Year diary entry based on this data:

🎧 Top Genres in Year:
{spotify_year_minutes.to_string()}

🎤 Top 3 Artists in Year:
{top_artists_year_minutes.to_string()}

🎶 Top 3 Songs in Year:
{top_songs_year_minutes.to_string()}

🌸 Weather Summary (Berlin):
{weather_summary_spring.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Year in Berlin:
{clothing_year}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate response from Gemini
response = model.generate_content(prompt)

# Display diary entry
print(response.text)


# %% [markdown]
# ## Monthly Diary Summary

# %%
# Step 1: Extract the current month from the dataset
current_month = spotify_df['month'].max()  # Assumes month column contains month names like 'April'

# Filter Spotify data for the current month
spotify_current_month = spotify_df[spotify_df['month'] == current_month]

# 🎵 Spotify Summary - Top 3 Genres by Listening Time in the Current Month
spotify_current_month_genres = spotify_current_month.groupby('main_genre')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

spotify_current_month_genres_minutes = (spotify_current_month_genres / 60000).round(2)
print(f"🎧 Top 3 Most Listened Genres in {current_month} (by Minutes):")
print(spotify_current_month_genres_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists in the Current Month
top_artists_current_month = spotify_current_month.groupby('artistName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

top_artists_current_month_minutes = (top_artists_current_month / 60000).round(2)
print(f"🎤 Top 3 Most Listened Artists in {current_month}:")
print(top_artists_current_month_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs in the Current Month
top_songs_current_month = spotify_current_month.groupby('trackName')['msPlayed'].sum() \
    .sort_values(ascending=False).head(3)

top_songs_current_month_minutes = (top_songs_current_month / 60000).round(2)
print(f"🎶 Top 3 Most Listened Songs in {current_month}:")
print(top_songs_current_month_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed for Berlin in the Current Month
weather_current_month = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['month'] == current_month)
].groupby('city')[['temp', 'precip', 'windspeed']].mean()

print(f"🌦️ Average Weather in Berlin during {current_month}:")
print(weather_current_month.to_string(float_format='%.1f'))

print("\n" + "-"*50 + "\n")

# 👕 Clothing Recommendation - Berlin in the Current Month
clothing_month = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['month'] == current_month)
]['clothing_recommendation'].dropna().unique()

print(f"👕 Clothing Recommendations for Berlin in {current_month}:")
for rec in clothing_month:
    print(f"- {rec}")


# %%
# # Month GEMINI API

# import google.generativeai as genai

# # Make sure GEMINI_API is defined
# genai.configure(api_key=GEMINI_API)

# # Load Gemini model
# model = genai.GenerativeModel("gemini-2.0-flash")

# # Create the Month prompt
# prompt = f"""
# Write a personal Year diary entry based on this data:

# 🎧 Top Genres in Current Month:
# {spotify_current_month_genres_minutes.to_string()}

# 🎤 Top 3 Artists in Current Month:
# {top_artists_current_month_minutes.to_string()}

# 🎶 Top 3 Songs in Current Month:
# {top_songs_current_month_minutes.to_string()}

# Weather Summary Current Month in (Berlin):
# {weather_current_month.to_string(float_format='%.1f')}

# 👕 Clothing Recommendations for Month in Berlin:
# {clothing_month}

# Make it casual, reflective, and maybe a bit poetic!
# """

# # Generate response from Gemini
# response = model.generate_content(prompt)

# # Display diary entry
# print(response.text)


import google.generativeai as genai

# Make sure GEMINI_API is defined
genai.configure(api_key=GEMINI_API)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Convert clothing recommendations array to a bullet-point string
clothing_text = "\n".join(f"- {item}" for item in clothing_month)

# Create the prompt with the current month name
prompt = f"""
Write a personal diary entry based on this data from {current_month}:

🎧 Top Genres in {current_month}:
{spotify_current_month_genres_minutes.to_string()}

🎤 Top 3 Artists in {current_month}:
{top_artists_current_month_minutes.to_string()}

🎶 Top 3 Songs in {current_month}:
{top_songs_current_month_minutes.to_string()}

🌦️ Weather Summary in Berlin during {current_month}:
{weather_current_month.to_string(float_format='%.1f')}

👕 Clothing Recommendations for Berlin in {current_month}:
{clothing_text}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate response from Gemini
response = model.generate_content(prompt)

# Display diary entry
print("\n📖 Gemini Diary Entry:\n")
print(response.text)



# %% [markdown]
# ## Week Diary Summary 

# %%
import pandas as pd

# Get the last date in the dataset
last_date = spotify_df['date'].max()

# Align to the last full Sunday
end_of_week = last_date - pd.to_timedelta(last_date.weekday() % 7, unit='D') + pd.Timedelta(days=6)
start_of_week = end_of_week - pd.Timedelta(days=6)

# Only call .date() if the object is a datetime
print(f"📅 Week range: {start_of_week} to {end_of_week}")


# %%
import pandas as pd
from datetime import timedelta

# Ensure 'datetime' column is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])

# Extract only the date (no time part) into a new column
weather_df['date'] = weather_df['datetime'].dt.date

# Find the most recent date in your dataset
latest_date = weather_df['date'].max()

# Convert to a pandas Timestamp
latest_date = pd.to_datetime(latest_date)

# Find the most recent *full* week ending on Sunday
# If today is not Sunday, roll back to the most recent one
days_since_sunday = (latest_date.weekday() + 1) % 7
last_sunday = latest_date - timedelta(days=days_since_sunday)

# Get Monday of that same week
last_monday = last_sunday - timedelta(days=6)

# Filter the dataframe to that full week
mask = (weather_df['datetime'].dt.date >= last_monday.date()) & \
       (weather_df['datetime'].dt.date <= last_sunday.date())
weather_last_week = weather_df[mask]

print(f"Most recent full week: {last_monday.date()} to {last_sunday.date()}")
print(weather_last_week.head())


# %%
import pandas as pd

import pandas as pd

# Step 1: Get the last date and align to the most recent full Sunday–Saturday week
last_date = spotify_df['date'].max()
end_of_week = last_date - pd.to_timedelta(last_date.weekday() % 7, unit='D') + pd.Timedelta(days=6)
start_of_week = end_of_week - pd.Timedelta(days=6)

# Filter Spotify data for the current (last full) week
spotify_week = spotify_df[
    (spotify_df['date'] >= start_of_week) & (spotify_df['date'] <= end_of_week)
]

# 🎧 Spotify Summary - Top 3 Genres by Listening Time in the Current Week
spotify_week_genres = spotify_week.groupby('main_genre')['msPlayed'].sum().sort_values(ascending=False).head(3)
spotify_week_genres_minutes = (spotify_week_genres / 60000).round(2)

print(f"📅 Week Range: {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}")
print(f"🎧 Top 3 Most Listened Genres This Week (Minutes):")
print(spotify_week_genres_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Most Listened Artists This Week
top_artists_week = spotify_week.groupby('artistName')['msPlayed'].sum().sort_values(ascending=False).head(3)
top_artists_week_minutes = (top_artists_week / 60000).round(2)

print(f"🎤 Top 3 Most Listened Artists This Week:")
print(top_artists_week_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Most Listened Songs This Week
top_songs_week = spotify_week.groupby('trackName')['msPlayed'].sum().sort_values(ascending=False).head(3)
top_songs_week_minutes = (top_songs_week / 60000).round(2)

print(f"🎶 Top 3 Most Listened Songs This Week:")
print(top_songs_week_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary - Avg Temp, Precip, Windspeed for Berlin in the Current Week
weather_week = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['date'] >= start_of_week) & (weather_df['date'] <= end_of_week)
]

weather_week_summary = weather_week.groupby('city')[['temp', 'precip', 'windspeed']].mean()

print(f"🌦️ Average Weather in Berlin ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}):")
print(weather_week_summary.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation for the Most Recent Week in Berlin
clothing_week = weather_week['clothing_recommendation'].dropna().unique()

print(f"👕 Clothing Recommendations for Berlin ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}):")
if len(clothing_week) > 0:
    for item in clothing_week:
        print(f"- {item}")
else:
    print("- No clothing recommendation found for the week.")



# %%
# Prepare clothing recommendations string
clothing_recs_text = "\n".join(f"- {rec}" for rec in clothing_week) if len(clothing_week) > 0 else "- No clothing recommendations available."

# Create the updated prompt
prompt = f"""
Write a personal weekly diary entry based on this data:

🗓️ Week: {start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}

🎧 Top Genres of the Week:
{spotify_week_genres_minutes.to_string()}

🎤 Top 3 Artists of the Week:
{top_artists_week_minutes.to_string()}

🎶 Top 3 Songs of the Week:
{top_songs_week_minutes.to_string()}

🌦️ Weather in Berlin this Week:
{weather_week_summary.to_string(float_format='%.1f')}

👕 Clothing Recommendations in Berlin this Week:
{clothing_recs_text}

Make it casual, reflective, and maybe a bit poetic!
"""

# Generate Gemini response
response = model.generate_content(prompt)

# Output the diary entry
print("\n📖 Weekly Diary Entry:\n")
print(response.text)


# %% [markdown]
# ## Day Dairy Summery 

# %%
# Step 1: Get the most recent date in the dataset
latest_date = spotify_df['date'].max()

# Filter Spotify and Weather data for the most recent day
spotify_today = spotify_df[spotify_df['date'] == latest_date]
weather_today = weather_df[
    (weather_df['date'] == latest_date) &
    (weather_df['city'].str.lower().str.strip() == 'berlin')
]

# 🎧 Spotify Summary - Top 3 Genres by Listening Time Today
spotify_today_genres = spotify_today.groupby('main_genre')['msPlayed'].sum().sort_values(ascending=False).head(3)
spotify_today_genres_minutes = (spotify_today_genres / 60000).round(2)
print(f"🎧 Top 3 Most Listened Genres on {latest_date.strftime('%Y-%m-%d')} (by Minutes):")
print(spotify_today_genres_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎤 Top 3 Artists Today
top_artists_today = spotify_today.groupby('artistName')['msPlayed'].sum().sort_values(ascending=False).head(3)
top_artists_today_minutes = (top_artists_today / 60000).round(2)
print(f"🎤 Top 3 Most Listened Artists on {latest_date.strftime('%Y-%m-%d')}:")
print(top_artists_today_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🎶 Top 3 Songs Today
top_songs_today = spotify_today.groupby('trackName')['msPlayed'].sum().sort_values(ascending=False).head(3)
top_songs_today_minutes = (top_songs_today / 60000).round(2)
print(f"🎶 Top 3 Most Listened Songs on {latest_date.strftime('%Y-%m-%d')}:")
print(top_songs_today_minutes.to_string())

print("\n" + "-"*50 + "\n")

# 🌦️ Weather Summary for Berlin Today
weather_today_summary = weather_today.groupby('city')[['temp', 'precip', 'windspeed']].mean()
print(f"🌦️ Weather in Berlin on {latest_date.strftime('%Y-%m-%d')}:")
print(weather_today_summary.to_string(float_format='%.1f'))

# 👕 Clothing Recommendation for Berlin Today
clothing_today = weather_today['clothing_recommendation'].dropna().unique()
print(f"\n👕 Clothing Recommendations for Berlin on {latest_date.strftime('%Y-%m-%d')}:")
if clothing_today.size > 0:
    for rec in clothing_today:
        print(f"- {rec}")
else:
    print("- No clothing recommendation available.")


# %%
# 👕 Clothing Recommendation for Berlin Today
clothing_today = weather_today['clothing_recommendation'].dropna().unique()
clothing_text = "\n".join(f"- {rec}" for rec in clothing_today) if len(clothing_today) > 0 else "- No recommendation available."

# Prompt for Gemini
prompt = f"""
Write a personal daily diary entry based on this data:

🗓️ Date: {latest_date.strftime('%Y-%m-%d')}

🎧 Top Genres Today:
{spotify_today_genres_minutes.to_string()}

🎤 Top 3 Artists Today:
{top_artists_today_minutes.to_string()}

🎶 Top 3 Songs Today:
{top_songs_today_minutes.to_string()}

🌤️ Weather in Berlin:
{weather_today_summary.to_string(float_format='%.1f')}

👕 Clothing Recommendations:
{clothing_text}

Make it casual, reflective, and maybe a bit poetic!
"""

# Step 5: Generate and print diary entry
response = model.generate_content(prompt)
print("\n📖 Daily Diary Entry:\n")
print(response.text)
# %%
import streamlit as st
import datetime as dt
from utils.weather import get_weather
from spotify_loader import load_spotify_data
import os
import requests
from dotenv import load_dotenv
import pandas as pd 
import numpy  as np
import matplotlib.pyplot as plt
import statistics as st
import seaborn as sns
# from utils.spotify_data import load_spotify_data, get_today_songs
# from utils.spotify_genre import get_artist_genre


# %%
from api_key import Weather_API

# %%
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

# %%
# Replace with your actual file path
weather_df = pd.read_csv('merged_weather_data.csv')

# %%
print(weather_df['city'].unique())


# %%
weather_df.columns

# %%
# Drop the 'name' column if it exists
if 'city.1' in weather_df.columns:
    merged_weather_df = weather_df.drop(columns=['city.1'])
    print("✅ 'city.1' column dropped.")
else:
    print("ℹ️ No 'city.1' column found to drop.")


# %%
#weather_df

# %%
merged_weather_df[['datetime', 'city', 'temp', 'clothing_recommendation']].head()


# %% [markdown]
# # Adding Season Column

# %%
import pandas as pd

def add_season_column(weather_df, date_column='datetime'):
    """
    Adds a 'season' column based on the month in a datetime column.
    Assumes Northern Hemisphere seasons.
    """
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Autumn"

    # Ensure datetime column is in datetime format
    weather_df[date_column] = pd.to_datetime(weather_df[date_column], errors='coerce')

    # Apply the season logic
    weather_df['season'] = weather_df[date_column].dt.month.apply(get_season)

    return weather_df

# 🧠 Load your CSV
weather_df = pd.read_csv("merged_weather_data.csv")

# 🍁 Add season info
weather_df = add_season_column(weather_df)

# 💾 Save back to CSV
weather_df.to_csv("merged_weather_data.csv", index=False)



# %%
# Convert sunrise and sunset to datetime.time format if they're strings
weather_df['sunrise'] = pd.to_datetime(weather_df['sunrise'], errors='coerce').dt.time
weather_df['sunset'] = pd.to_datetime(weather_df['sunset'], errors='coerce').dt.time

# %%
# Convert time objects to datetime and extract hour
weather_df['sunrise_hour'] = pd.to_datetime(weather_df['sunrise'], format='%H:%M:%S', errors='coerce').dt.hour
weather_df['sunset_hour'] = pd.to_datetime(weather_df['sunset'], format='%H:%M:%S', errors='coerce').dt.hour

# %%
weather_df['sunrise_hour'] = weather_df['sunrise'].apply(lambda x: x.hour if pd.notnull(x) else None)
weather_df['sunset_hour'] = weather_df['sunset'].apply(lambda x: x.hour if pd.notnull(x) else None)

# %%
# Filter for summer
summer_recommendations = weather_df[weather_df['season'] == 'Autumn']

# View relevant columns
print(summer_recommendations[['datetime', 'city', 'temp', 'clothing_recommendation']].head())


# %%
print(weather_df[['temp', 'humidity', 'conditions', 'uvindex', 'windspeed', 'clothing_recommendation']].sample(5))


# %% [markdown]
# ## WEATHER EDA

# %%
# Basic info
print("\nℹ️ Data Info:")
print(weather_df.info())

# %%
# Descriptive statistics
print("\n📊 Summary Stats:")
print(weather_df.describe(include='all'))

# %%
# Step 1: Check for missing values
print("\n❓ Missing Values (Before):")
print(weather_df.isnull().sum())

# Step 2: Fill missing numeric columns with mean
numeric_cols = weather_df.select_dtypes(include='number').columns
weather_df[numeric_cols] = weather_df[numeric_cols].fillna(weather_df[numeric_cols].mean())

# Step 3: Fill missing string/object columns with 'Unknown'
object_cols = weather_df.select_dtypes(include='object').columns
weather_df[object_cols] = weather_df[object_cols].fillna("Unknown")

# Step 4: Re-check for missing values
print("\n✅ Missing Values (After Fill):")
print(weather_df.isnull().sum())


# %%
# Ensure 'temp' column has valid numeric values
weather_df['temp'] = pd.to_numeric(weather_df['temp'], errors='coerce')

# Drop rows where temp is NaN (optional but helps avoid errors)
weather_df = weather_df.dropna(subset=['temp'])

# Find the hottest day
hottest_day = weather_df.loc[weather_df['temp'].idxmax()]
print("🔥 Hottest Day Overall:")
print(hottest_day)


# %%
coldest_day = weather_df.loc[weather_df['temp'].idxmin()]
print("❄️ Coldest Day Overall:")
print(coldest_day[['datetime', 'temp', 'city', 'conditions', 'clothing_recommendation']])



# %%
# Filter for Berlin only
berlin_weather = weather_df[weather_df['city'] == 'Berlin']

# Find the row with the lowest temperature
coldest_day = berlin_weather.loc[berlin_weather['temp'].idxmin()]

# Display the result
print("❄️ Coldest Day in Berlin:")
print(coldest_day[['datetime', 'temp', 'conditions', 'description', 'clothing_recommendation']])


# %%
hottest_berlin = weather_df[weather_df['city'] == 'Berlin'].loc[
    weather_df[weather_df['city'] == 'Berlin']['temp'].idxmax()
]

print("🔥 Hottest Day in Berlin:")
print(hottest_berlin[['datetime', 'temp', 'conditions', 'clothing_recommendation']])


# %%
# Make sure 'precip' is numeric
weather_df['precip'] = pd.to_numeric(weather_df['precip'], errors='coerce')

# Drop rows with NaN in 'precip'
rain_data = weather_df.dropna(subset=['precip'])

# Find the most rainy day
most_rainy_day = rain_data.loc[rain_data['precip'].idxmax()]

# Display result
print("🌧️ Most Rainy Day:")
print(most_rainy_day[['datetime', 'city', 'precip', 'conditions', 'clothing_recommendation']])


# %%
# Ensure 'precip' is numeric
weather_df['precip'] = pd.to_numeric(weather_df['precip'], errors='coerce')

# Filter for Berlin only
berlin_data = weather_df[merged_weather_df['city'].str.lower().str.strip() == 'berlin']

# Drop NaNs in precip
berlin_data = berlin_data.dropna(subset=['precip'])

# Get the most rainy day in Berlin
most_rainy_berlin = berlin_data.loc[berlin_data['precip'].idxmax()]

# Display
print("🌧️ Most Rainy Day in Berlin:")
print(most_rainy_berlin[['datetime', 'precip', 'conditions', 'clothing_recommendation']])


# %%
# Filter Berlin data
berlin_data = weather_df[weather_df['city'].str.lower().str.strip() == 'berlin']

# Ensure 'precip' is numeric
berlin_data['precip'] = pd.to_numeric(berlin_data['precip'], errors='coerce')

# Filter rows with snow in the condition
snow_days = berlin_data[berlin_data['conditions'].str.lower().str.contains('snow', na=False)]

# Drop rows with missing precip
snow_days = snow_days.dropna(subset=['precip'])

# Get the snow day with the highest precipitation
most_snowed_day = snow_days.loc[snow_days['precip'].idxmax()]

# Display
print("❄️ Most Snowed Day in Berlin:")
print(most_snowed_day[['datetime', 'precip', 'conditions', 'clothing_recommendation']])


# %%
# Filter Berlin data
berlin_data = weather_df[weather_df['city'].str.lower().str.strip() == 'berlin']

# Ensure windspeed column is numeric
berlin_data['windspeed'] = pd.to_numeric(berlin_data['windspeed'], errors='coerce')

# Drop rows with missing windspeed
berlin_data = berlin_data.dropna(subset=['windspeed'])

# Find the row with the highest windspeed
most_windy_day = berlin_data.loc[berlin_data['windspeed'].idxmax()]

# Display the result
print("💨 Most Windy Day in Berlin:")
print(most_windy_day[['datetime', 'windspeed', 'conditions', 'clothing_recommendation']])


# %%
# Filter lagos data
berlin_data = weather_df[weather_df['city'].str.lower().str.strip() == 'lagos']

# Ensure windspeed column is numeric
berlin_data['windspeed'] = pd.to_numeric(berlin_data['windspeed'], errors='coerce')

# Drop rows with missing windspeed
berlin_data = berlin_data.dropna(subset=['windspeed'])

# Find the row with the highest windspeed
most_windy_day = berlin_data.loc[berlin_data['windspeed'].idxmax()]

# Display the result
print("💨 Most Windy Day in Lagos:")
print(most_windy_day[['datetime', 'windspeed', 'conditions', 'clothing_recommendation']])

# %%
# Ensure datetime is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter Berlin and summer months (June, July, August)
summer_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['datetime'].dt.month.isin([6, 7, 8]))
]

# Get unique clothing recommendations
summer_recommendations = summer_berlin['clothing_recommendation'].dropna().unique()

print("👕 Clothing Recommendations for Summer in Berlin:")
for rec in summer_recommendations:
    print(f"- {rec}")


# %%
# Ensure datetime is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter Berlin and summer months (June, July, August)
summer_berlin = merged_weather_df[
    (weather_df['city'].str.lower().str.strip() == 'lagos') &
    (weather_df['datetime'].dt.month.isin([6, 7, 8]))
]

# Get unique clothing recommendations
summer_recommendations = summer_berlin['clothing_recommendation'].dropna().unique()

print("👕 Clothing Recommendations for Summer in Lagos:")
for rec in summer_recommendations:
    print(f"- {rec}")

# %%
# Ensure datetime column is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter for Berlin in spring months: March, April, May
spring_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['datetime'].dt.month.isin([3, 4, 5]))
]

# Drop missing clothing recommendations
spring_recommendations = spring_berlin['clothing_recommendation'].dropna().unique()

# Display
print("🌸 Clothing Recommendations for Spring in Berlin:")
for rec in spring_recommendations:
    print(f"- {rec}")


# %%
# Ensure datetime column is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter for Lagos in spring months: March, April, May
spring_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'lagos') &
    (weather_df['datetime'].dt.month.isin([3, 4, 5]))
]

# Drop missing clothing recommendations
spring_recommendations = spring_berlin['clothing_recommendation'].dropna().unique()

# Display
print("🌸 Clothing Recommendations for Spring in Lagos:")
for rec in spring_recommendations:
    print(f"- {rec}")

# %%
# Ensure datetime column is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter for Tokyo in spring months: March, April, May
spring_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'tokyo') &
    (weather_df['datetime'].dt.month.isin([3, 4, 5]))
]

# Drop missing clothing recommendations
spring_recommendations = spring_berlin['clothing_recommendation'].dropna().unique()

# Display
print("🌸 Clothing Recommendations for Spring in Tokyo:")
for rec in spring_recommendations:
    print(f"- {rec}")

# %%
# Convert datetime if needed
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter windy days in Berlin (e.g., windspeed > 20)
windy_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df.get('windspeed', 0) > 20)
]

# Get unique clothing recommendations
windy_recommendations = windy_berlin['clothing_recommendation'].dropna().unique()

# Display recommendations
print("💨 Clothing Recommendations for Windy Days in Berlin:")
for rec in windy_recommendations:
    print(f"- {rec}")


# %%
# Convert datetime if needed
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], errors='coerce')

# Filter windy days in Lagos (e.g., windspeed > 20)
windy_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'lagos') &
    (weather_df.get('windspeed', 0) > 20)
]

# Get unique clothing recommendations
windy_recommendations = windy_berlin['clothing_recommendation'].dropna().unique()

# Display recommendations
print("💨 Clothing Recommendations for Windy Days in Lagos:")
for rec in windy_recommendations:
    print(f"- {rec}")


# %%
# Make sure windspeed column exists and is numeric
weather_df['windspeed'] = pd.to_numeric(weather_df.get('windspeed', 0), errors='coerce')

# Group by city and calculate max windspeed per city
max_wind_by_city = weather_df.groupby('city')['windspeed'].max().sort_values(ascending=False)

# Get the city with the highest recorded windspeed
most_windy_city = max_wind_by_city.idxmax()
max_wind_speed = max_wind_by_city.max()

print(f"🌬️ Most Windy City: {most_windy_city} with windspeed of {max_wind_speed} km/h")


# %%
import pandas as pd

# Ensure windspeed is numeric and datetime is in datetime format
weather_df['windspeed'] = pd.to_numeric(weather_df['windspeed'], errors='coerce')
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])

# Filter for Berlin
berlin_data = weather_df[weather_df['city'].str.strip().str.lower() == 'berlin']

# Drop any rows with NaN windspeed
berlin_data = berlin_data.dropna(subset=['windspeed'])

# Find the most windy day
most_windy_day = berlin_data.loc[berlin_data['windspeed'].idxmax()]

# Display key information
print("🌬️ Most Windy Day in Berlin:")
print(most_windy_day[['datetime', 'windspeed', 'temp', 'conditions', 'clothing_recommendation']])


# %%
# Convert 'conditions' to lowercase for consistent comparison
weather_df['conditions'] = weather_df['conditions'].str.lower()

# Filter for snow-related conditions
snow_data = weather_df[weather_df['conditions'].str.contains('snow', na=False)]

# Count snow events per city
most_snowing_city = snow_data['city'].value_counts().idxmax()
snow_count = snow_data['city'].value_counts().max()

print(f"❄️ Most Snowing City: {most_snowing_city} with {snow_count} snow-related entries")


# %%
import pandas as pd

# Ensure datetime column is in datetime format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])

# Filter for Berlin and snow conditions
berlin_snow = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['conditions'].str.lower().str.contains('snow', na=False))
]

# Extract date from datetime
berlin_snow['date'] = berlin_snow['datetime'].dt.date

# Option 1: Count number of snow entries per day
snowiest_day = berlin_snow['date'].value_counts().idxmax()
entries = berlin_snow['date'].value_counts().max()

# Option 2 (if you have precip column): Total snowfall per day
# snowiest_day = berlin_snow.groupby('date')['precip'].sum().idxmax()
# total_snow = berlin_snow.groupby('date')['precip'].sum().max()

print(f"❄️ Most Snowing Day in Berlin: {snowiest_day} with {entries} snow records")


# %%
# Filter for Berlin on snowing days
berlin_snow = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['conditions'].str.lower().str.contains('snow', na=False))
]

# Show unique clothing recommendations on snow days
snow_clothing_recommendations = berlin_snow['clothing_recommendation'].value_counts()

print("🧣 Clothing Recommendations on Snowing Days in Berlin:")
print(snow_clothing_recommendations)


# %%
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# Step 1: Get the min temperature per city across all days
min_temp_by_city = weather_df.groupby('city')['temp'].min().reset_index()

# Step 2: Sort to find the coldest
min_temp_by_city = min_temp_by_city.sort_values(by='temp')

# Step 3: Plot
plt.figure(figsize=(10, 5))
sns.barplot(data=min_temp_by_city, x='city', y='temp', palette="Blues")

# Step 4: Highlight the coldest one
coldest = min_temp_by_city.iloc[0]
plt.text(
    x=0,
    y=coldest['temp'] - 1,
    s=f"❄️ Coldest: {coldest['city']} ({coldest['temp']})",
    fontsize=12,
    color='blue',
    weight='bold'
)

# Final touches
plt.title("❄️ Coldest City Based on Min Recorded Temperature", fontsize=15)
plt.ylabel("Min Temp")
plt.xlabel("City")
plt.tight_layout()
plt.show()


# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Get the max temperature per city across all days
max_temp_by_city = weather_df.groupby('city')['temp'].max().reset_index()

# Step 2: Sort to find the hottest
max_temp_by_city = max_temp_by_city.sort_values(by='temp', ascending=False)

# Step 3: Plot
plt.figure(figsize=(10, 5))
sns.barplot(data=max_temp_by_city, x='city', y='temp', palette="Reds")

# Step 4: Highlight the hottest one
hottest = max_temp_by_city.iloc[0]
plt.text(
    x=0,
    y=hottest['temp'] + 1,
    s=f"🔥 Hottest: {hottest['city']} ({hottest['temp']}°C)",
    fontsize=12,
    color='darkred',
    weight='bold'
)

# Final touches
plt.title("🔥 Hottest City Based on Max Recorded Temperature", fontsize=15)
plt.ylabel("Max Temp (°C)")
plt.xlabel("City")
plt.tight_layout()
plt.show()


# %%
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# Filter for Lagos
lagos_df = weather_df[merged_weather_df['city'] == 'Berlin']

# Find the coldest day
coldest_day = lagos_df.loc[lagos_df['temp'].idxmin()]

# Plot all 14 days for Lagos
plt.figure(figsize=(12, 6))
sns.lineplot(data=lagos_df, x='datetime', y='temp', marker='o', color='blue')

# Annotate the coldest day
plt.axvline(x=coldest_day['datetime'], color='red', linestyle='--')
plt.text(
    coldest_day['datetime'],
    coldest_day['temp'] + 0.5,
    f"❄️ Coldest: {coldest_day['temp']}°C",
    color='red',
    fontsize=12,
    weight='bold'
)

# Final touches
plt.title("Coldest Day in Berlin)", fontsize=15)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# Filter for Berlin and Lagos
berlin_lagos_seasonal = weather_df[weather_df['city'].isin(['Berlin', 'Lagos'])]

# Group by city and season, then calculate average temperature
season_avg_temp = (
    berlin_lagos_seasonal
    .groupby(['city', 'season'])['temp']  # Make sure this matches your actual temp column
    .mean()
    .reset_index()
)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=season_avg_temp,
    x='season',
    y='temp',
    hue='city',
    palette='Spectral'
)

plt.title("🌤️ Average Temperature per Season: Berlin & Lagos", fontsize=15)
plt.xlabel("Season")
plt.ylabel("Avg Temp (°C)")
plt.tight_layout()
plt.show()



# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Filter only Berlin and Lagos
berlin_lagos = weather_df[weather_df['city'].isin(['Berlin', 'Lagos'])]

# Group by city and season, then compute average humidity
season_avg_humidity = (
    berlin_lagos
    .groupby(['city', 'season'])['humidity']
    .mean()
    .reset_index()
)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=season_avg_humidity,
    x='season',
    y='humidity',
    hue='city',
    palette='Blues'
)

plt.title("💧 Average Humidity per Season: Berlin vs Lagos", fontsize=15)
plt.xlabel("Season")
plt.ylabel("Average Humidity (%)")
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt

# Ensure datetime column is in proper format
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])

# Filter Berlin data
berlin_data = weather_df[weather_df['city'].str.lower().str.strip() == 'berlin']

# Handle case when no data for Berlin
if berlin_data.empty:
    print("No weather data available for Berlin.")
else:
    # Find the hottest day
    hottest_day_row = berlin_data.loc[berlin_data['temp'].idxmax()]

    # Extract details safely
    #temp = hottest_day_row['temp']
    #date = hottest_day_row['datetime'].date()
    condition = hottest_day_row.get('conditions', 'Unknown')
    recommendation = hottest_day_row.get('clothing_recommendation', 'No data')

    # Create a simple bar chart
    plt.figure(figsize=(6, 6))
    plt.bar("Hottest Day", temp, color="orangered")

    # Annotate with clothing advice
    plt.text(0, temp + 1,
             f"{temp:.1f}°C\n{date}\n{condition}\n{recommendation}",
             ha='center', fontsize=10)

    plt.title("🔥 Hottest Day in Berlin")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Define threshold for "hot" days (e.g., > 29°C)
hot_threshold = 29

# Filter for hot days in Berlin
hot_berlin = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['temp'] > hot_threshold)
]

# Group by clothing recommendation and count
hot_recommendations = (
    hot_berlin.groupby('clothing_recommendation')
    .size()
    .reset_index(name='count')
    .sort_values(by='count', ascending=False)
)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=hot_recommendations,
    y='clothing_recommendation',
    x='count',
    palette='YlOrRd'
)

plt.title("Clothing Recommendations on Hot Days in Berlin", fontsize=14)
plt.xlabel("Frequency")
plt.ylabel("Clothing Recommendation")
plt.tight_layout()
plt.show()


# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Filter only Berlin data
berlin_data = weather_df[weather_df['city'].str.strip().str.lower() == 'berlin']

# Group and count clothing recommendations by season
seasonal_clothing = (
    berlin_data
    .groupby(['season', 'clothing_recommendation'])
    .size()
    .reset_index(name='count')
)


# %%
# Plot the grouped clothing recommendation data by season
plt.figure(figsize=(12, 6))
sns.barplot(
    data=seasonal_clothing,
    x='season',
    y='count',
    hue='clothing_recommendation',
    palette='Set2'
)

plt.title("Clothing Recommendations by Season in Berlin", fontsize=14)
plt.xlabel("Season")
plt.ylabel("Count")
plt.legend(title='Clothing Recommendation', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter Berlin data
berlin_data = weather_df[weather_df['city'].str.strip().str.lower() == 'berlin']

# Group and count clothing recommendations by season
seasonal_clothing = (
    berlin_data
    .groupby(['season', 'clothing_recommendation'])
    .size()
    .reset_index(name='count')
)

# Filter for Spring only
spring_clothing = seasonal_clothing[seasonal_clothing['season'].str.lower() == 'spring']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=spring_clothing,
    y='clothing_recommendation',
    x='count',
    palette='BuGn'
)

plt.title("Clothing Recommendations in Spring (Berlin)", fontsize=14)
plt.xlabel("Frequency")
plt.ylabel("Clothing Recommendation")
plt.tight_layout()
plt.show()




# %%
# Filter Berlin data
berlin_data = weather_df[weather_df['city'].str.strip().str.lower() == 'berlin']

# Group and count clothing recommendations by season
seasonal_clothing = (
    berlin_data
    .groupby(['season', 'clothing_recommendation'])
    .size()
    .reset_index(name='count')
)

# Filter for Summer only
summer_clothing = seasonal_clothing[seasonal_clothing['season'].str.lower() == 'summer']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=summer_clothing,
    y='clothing_recommendation',
    x='count',
    palette='YlOrRd'
)

plt.title("☀️ Clothing Recommendations in Summer (Berlin)", fontsize=14)
plt.xlabel("Frequency")
plt.ylabel("Clothing Recommendation")
plt.tight_layout()
plt.show()


# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Filter only Berlin and Lagos data
berlin_lagos = weather_df[weather_df['city'].isin(['Berlin', 'Lagos'])]

# Group and count clothing recommendations by city and season
seasonal_clothing = (
    berlin_lagos
    .groupby(['season', 'city', 'clothing_recommendation'])
    .size()
    .reset_index(name='count')
)

# Filter for summer only
summer_clothing = seasonal_clothing[seasonal_clothing['season'].str.lower() == 'summer']

# Create combined barplot
plt.figure(figsize=(14, 6))
sns.barplot(
    data=summer_clothing,
    x='city',
    y='count',
    hue='clothing_recommendation',
    palette='Set2',
    dodge=True
)

plt.title("☀️ Clothing Recommendations in Summer: Berlin vs Lagos", fontsize=14)
plt.xlabel("City")
plt.ylabel("Recommendation Count")
plt.legend(title="Recommendation", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Filter only Berlin and Lagos data
berlin_lagos = weather_df[weather_df['city'].isin(['Berlin', 'Lagos'])]

# Group and count clothing recommendations by city and season
seasonal_clothing = (
    berlin_lagos
    .groupby(['season', 'city', 'clothing_recommendation'])
    .size()
    .reset_index(name='count')
)

# Filter for summer only
summer_clothing = seasonal_clothing[seasonal_clothing['season'].str.lower() == 'spring']

# Create combined barplot
plt.figure(figsize=(14, 6))
sns.barplot(
    data=summer_clothing,
    x='city',
    y='count',
    hue='clothing_recommendation',
    palette='Set2',
    dodge=True
)

plt.title("☀️ Clothing Recommendations in Spring: Berlin vs Lagos", fontsize=14)
plt.xlabel("City")
plt.ylabel("Recommendation Count")
plt.legend(title="Recommendation", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Filter for Berlin and Lagos
cities = ['Berlin', 'Lagos']
city_data = weather_df[weather_df['city'].isin(cities)]

# Get hottest day per city
hottest_per_city = city_data.loc[city_data.groupby('city')['temp'].idxmax()]

# Reset index for plotting
hottest_per_city = hottest_per_city.reset_index(drop=True)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=hottest_per_city,
    x='city',
    y='temp',
    palette='YlOrRd'
)

# Annotate clothing recommendations
for i, row in hottest_per_city.iterrows():
    plt.text(
        i,
        row['temp'] + 0.5,
        f"{row['temp']}°C\n👕 {row['clothing_recommendation']}",
        ha='center',
        fontsize=10,
        color='black'
    )

plt.title("🔥 Hottest Day & Clothing Recommendation: Berlin vs Lagos", fontsize=14)
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter for Berlin and Lagos
cities = ['Berlin', 'Lagos']
city_dat = weather_df[weather_df['city'].isin(cities)]

# Get coldest day per city
Coldest_per_city = city_dat.loc[city_dat.groupby('city')['temp'].idxmin()].reset_index(drop=True)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=Coldest_per_city,
    x='city',
    y='temp',
    palette='Blues_r'
)

# Annotate clothing recommendations
for i, row in Coldest_per_city.iterrows():
    plt.text(
        i,
        row['temp'] + 1,
        f"{row['temp']}°C\n {row['clothing_recommendation']}",
        ha='center',
        fontsize=10,
        color='black'
    )

plt.title("❄️ Coldest Day & Clothing Recommendation: Berlin vs Lagos", fontsize=14)
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()


# %%
print(weather_df[['sunrise', 'sunrise_hour']].dropna().head(10))


# %%
mask = weather_df['datetime'].dt.hour == weather_df['sunrise_hour']
print("Matching rows:", mask.sum())


# %%
berlin_sunrise_winter = weather_df[
    weather_df.apply(lambda row: abs(row['datetime'].hour - row['sunrise_hour']) <= 1 if pd.notnull(row['sunrise_hour']) else False, axis=1)
]


# %%
print("Records in berlin_sunrise_winter:", len(berlin_sunrise_winter))
print(berlin_sunrise_winter['clothing_recommendation'].value_counts())


# %%
# Display first 50 non-null rows of 'datetime' and 'sunrise' for debugging
print(weather_df[['datetime', 'sunrise']].dropna().head(10))

# %%
# Show extracted hour alongside original data
print(weather_df[['datetime', 'sunrise', 'sunrise_hour']].dropna().head(10))


# %%
# Make sure sunrise is parsed as a time (if it's not already)
weather_df['sunrise'] = pd.to_datetime(weather_df['sunrise'], format='%H:%M:%S').dt.time

# Extract the hour from datetime for comparison
weather_df['datetime_hour'] = weather_df['datetime'].dt.hour


# %%
# Match rows where the datetime's hour equals the sunrise hour
sunrise_clothing = weather_df[weather_df['datetime_hour'] == weather_df['sunrise_hour']]


# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Filter for Berlin and Lagos
cities = ['Berlin', 'Lagos']
city_data = weather_df[weather_df['city'].isin(cities)]

# Filter for rainy days — adjust depending on your exact column values
rainy_data = city_data[city_data['conditions'].str.lower().str.contains('rain')]

# Get the most rainy day per city (you could also use max precipitation if available)
rainiest_day_per_city = rainy_data.loc[rainy_data.groupby('city')['datetime'].idxmin()].reset_index(drop=True)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=rainiest_day_per_city,
    x='city',
    y='temp',  # or use 'precipitation' if available
    palette='Blues_r'
)

# Annotate clothing recommendations
for i, row in rainiest_day_per_city.iterrows():
    plt.text(
        i,
        row['temp'] + 1,
        f"{row['temp']}°C\n☔ {row['clothing_recommendation']}",
        ha='center',
        fontsize=10,
        color='black'
    )

plt.title("☔ Rainy Day & Clothing Recommendation: Berlin vs Lagos", fontsize=14)
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt

# Filter for Berlin and Summer
berlin_summer = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'berlin') &
    (weather_df['season'].str.lower() == 'summer')
]

# Count clothing recommendations
summer_rec_counts = berlin_summer['clothing_recommendation'].value_counts().reset_index()
summer_rec_counts.columns = ['clothing_recommendation', 'count']

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(
    summer_rec_counts['count'],
    labels=summer_rec_counts['clothing_recommendation'],
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Pastel1.colors,
    wedgeprops=dict(width=0.5)
)

plt.title("👕 Clothing Recommendations in Summer (Berlin)", fontsize=14)
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt

# Filter for Lagos and Summer
lagos_summer = weather_df[
    (weather_df['city'].str.lower().str.strip() == 'lagos') &
    (weather_df['season'].str.lower() == 'summer')
]

# Count clothing recommendations
summer_rec_counts_lagos = lagos_summer['clothing_recommendation'].value_counts().reset_index()
summer_rec_counts_lagos.columns = ['clothing_recommendation', 'count']

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(
    summer_rec_counts_lagos['count'],
    labels=summer_rec_counts_lagos['clothing_recommendation'],
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Pastel2.colors,
    wedgeprops=dict(width=0.5)
)

plt.title("👚 Clothing Recommendations in Summer (Lagos)", fontsize=14)
plt.tight_layout()
plt.show



# %% [markdown]
# # SPOTIFY DATA

# %%
import os
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def load_spotify_data(folder_path):
    records = []

    for filename in os.listdir(folder_path):
        if filename.startswith("StreamingHistory_music") and filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                data = json.load(f)
                records.extend(data)

    StreamingMusic = pd.DataFrame(records)
    StreamingMusic['endTime'] = pd.to_datetime(StreamingMusic['endTime'])
    return StreamingMusic

# Replace with your actual folder path
folder_path = "Spotify Account Data"

# Load data
spotify_df = load_spotify_data(folder_path)

# Print the entire DataFrame
print(spotify_df)

# If it’s too big and cuts off:
# Print first few rows
print(spotify_df.head())

# Print DataFrame shape
print("Shape:", spotify_df.shape)

# Print column names
print("Columns:", spotify_df.columns.tolist())

# Optional: Save to CSV to inspect
spotify_df.to_csv("spotify_streaming_cleaned.csv", index=False)


# %%
spotify_df.head()

# %%
# Get Artist Genres from Spotify
# -------------------------
def get_artist_genres(spotify_df):
    # Load API credentials
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    # Get unique artists
    unique_artists = spotify_df['artistName'].dropna().unique()
    artist_genres = {}

    for artist in unique_artists:
        if artist in artist_genres:
            continue  # skip if already cached
        try:
            result = sp.search(q=f"artist:{artist}", type="artist", limit=1)
            items = result['artists']['items']
            if items:
                artist_genres[artist] = items[0]['genres']
            else:
                artist_genres[artist] = []
            time.sleep(0.1)
        except Exception as e:
            artist_genres[artist] = []
            print(f"Error fetching genre for {artist}: {e}")

    return artist_genres

# -------------------------
# Apply Genre Info to DataFrame
# -------------------------
def assign_genres(spotify_df, artist_genres):
    spotify_df['genre'] = spotify_df['artistName'].map(lambda x: artist_genres.get(x, []))
    spotify_df['main_genre'] = spotify_df['genre'].apply(lambda x: x[0] if x else "Unknown")
    return spotify_df



# %%
# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":
    folder_path = "Spotify Account Data"
    spotify_df = load_spotify_data(folder_path)
    artist_genres = get_artist_genres(spotify_df)
    spotify_df = assign_genres(spotify_df, artist_genres)
spotify_df



# %%
    # Preview
print(spotify_df[['artistName', 'trackName', 'main_genre']].head())
print("Shape:", spotify_df.shape)
print("Columns:", spotify_df.columns.tolist())

    # Optional: Save to CSV
spotify_df.to_csv("spotify_streaming_cleaned.csv", index=False)

# %%
import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# -------------------------
# Load Spotify Data
# -------------------------
def load_spotify_data(folder_path):
    records = []
    for filename in os.listdir(folder_path):
        if filename.startswith("StreamingHistory_music") and filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                data = json.load(f)
                records.extend(data)
    spotify_df = pd.DataFrame(records)
    spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])
    return spotify_df





# %%
# -------------------------
# Fetch or Load Artist Genres (with caching)
# -------------------------
def get_artist_genres(spotify_df, cache_file="artist_genres_cache.json"):
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Missing Spotify API credentials. Check .env file.")

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    # Load cached genres if available
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            artist_genres = json.load(f)
    else:
        artist_genres = {}

    unique_artists = spotify_df['artistName'].dropna().unique()

    for artist in unique_artists:
        key = artist.strip().lower()
        if key in artist_genres:
            continue
        try:
            print(f"Searching for: '{artist}'")
            result = sp.search(q=f"artist:{artist.strip()}", type="artist", limit=1)
            items = result['artists']['items']
            if items:
                artist_genres[key] = items[0]['genres']
            else:
                artist_genres[key] = []
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching genre for {artist}: {e}")
            artist_genres[key] = []

    # Save cache
    with open(cache_file, "w") as f:
        json.dump(artist_genres, f)

    return artist_genres

# %%
# -------------------------
# Assign Genres to DataFrame
# -------------------------
def assign_genres(spotify_df, artist_genres):
    spotify_df['genre'] = spotify_df['artistName'].apply(lambda x: artist_genres.get(str(x).strip().lower(), []))
    spotify_df['main_genre'] = spotify_df['genre'].apply(lambda x: x[0] if x else "Unknown")
    return spotify_df


# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":
    folder_path = "Spotify Account Data"
    spotify_df = load_spotify_data(folder_path)

    artist_genres = get_artist_genres(spotify_df)
    spotify_df = assign_genres(spotify_df, artist_genres)

    # Preview
    print(spotify_df[['artistName', 'trackName', 'main_genre']].head())
    print("Shape:", spotify_df.shape)

    # Save cleaned data
    spotify_df.to_csv("spotify_streaming_cleaned.csv", index=False)

# %%
spotify_df

# %%
import pandas as pd

# Assuming your DataFrame is called spotify_df
# Step 1: Convert endTime to datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Step 2: Extract the month
spotify_df['month'] = spotify_df['endTime'].dt.month

# Step 3: Define a function to get season from month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

# Step 4: Create the season column
spotify_df['season'] = spotify_df['month'].apply(get_season)


# %% [markdown]
# # Spotify EDA

# %%
# Group by genre and sum msPlayed
genre_playtime = (
    spotify_df.groupby('genre')['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
)

# Convert msPlayed to hours (optional, easier to interpret)
genre_playtime['Hours Listened'] = genre_playtime['msPlayed'] / (1000 * 60 * 60)

# Display top genres
print(genre_playtime)


# %%
# If 'genre' is a list, explode it into separate rows
spotify_df = spotify_df.explode('genre')

# Now group by genre and sum playtime
genre_playtime = (
    spotify_df.groupby('genre')['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
)

# Convert msPlayed to hours
genre_playtime['Hours Listened'] = genre_playtime['msPlayed'] / (1000 * 60 * 60)

# Display top genres
print(genre_playtime)


# %%
# Ensure 'genre' column is a string
spotify_df['genre'] = spotify_df['genre'].astype(str)

# Group by genre and sum msPlayed
top_genres = (
    spotify_df.groupby('genre')['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to hours for better understanding
top_genres['Hours Listened'] = top_genres['msPlayed'] / (1000 * 60 * 60)

# Show top 5 genres
print(top_genres[['genre', 'Hours Listened']])


# %%
import pandas as pd

# Count how many times each genre appears
genre_counts = spotify_df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Show the most listened-to genre
most_listened_genre = genre_counts.iloc[0]
print("🎧 Most listened-to genre:", most_listened_genre['genre'])
print("Play count:", most_listened_genre['count'])

# Optional: Display top 5
print("\n🎶 Top 10 Genres:\n", genre_counts.head())


# %%
# Make sure genre column is string and filter devotional songs
spotify_df['genre'] = spotify_df['genre'].astype(str)
devotional_df = spotify_df[spotify_df['genre'].str.lower().str.contains('devotional')]

# Group by song and artist, sum msPlayed
top_devotional_songs = (
    devotional_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes for readability
top_devotional_songs['Minutes Played'] = top_devotional_songs['msPlayed'] / (1000 * 60)

# Show results
print(top_devotional_songs[['trackName', 'artistName', 'Minutes Played']])


# %%
# Ensure 'genre' column is treated as string
spotify_df['genre'] = spotify_df['genre'].astype(str)

# Print all unique genres
unique_genres = spotify_df['genre'].unique()

# Display
for genre in unique_genres:
    print(genre)

# %%
# Ensure genre and track/artist columns are strings
spotify_df['genre'] = spotify_df['genre'].astype(str)
spotify_df['trackName'] = spotify_df['trackName'].astype(str)
spotify_df['artistName'] = spotify_df['artistName'].astype(str)

# Filter for lullaby-related songs (by genre or name)
lullaby_df = spotify_df[
    spotify_df['genre'].str.lower().str.contains('lullaby') |
    spotify_df['trackName'].str.lower().str.contains('lullaby') |
    spotify_df['artistName'].str.lower().str.contains('lullaby')
]

# Group and sum by track and artist
top_lullabies = (
    lullaby_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_lullabies['Minutes Listened'] = top_lullabies['msPlayed'] / (1000 * 60)

# Display result
print(top_lullabies[['trackName', 'artistName', 'Minutes Listened']])

# %%
# Replace 'trackName' with the actual column name in your dataset for the song title
most_played = spotify_df['trackName'].value_counts().reset_index()
most_played.columns = ['trackName', 'count']

# Display the top song
top_song = most_played.iloc[0]
print(f"🎶 Most Listened Song: {top_song['trackName']} ({top_song['count']} times)")


# %%
print(most_played.head(10))


# %%
# Group by season, trackName, and artistName to count plays
seasonal_top_songs = (
    spotify_df.groupby(['season', 'trackName', 'artistName'])
    .size()
    .reset_index(name='count')
)

# Get top song per season
top_per_season = (
    seasonal_top_songs.sort_values('count', ascending=False)
    .groupby('season')
    .first()
    .reset_index()
)

# Display
print(top_per_season)


# %%
import pandas as pd

# Ensure 'endTime' is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract just the date
spotify_df['date'] = spotify_df['endTime'].dt.date

# Find the day with the most tracks played
top_day = spotify_df['date'].value_counts().idxmax()
top_day_count = spotify_df['date'].value_counts().max()

print(f"📅 Most listened day: {top_day} with {top_day_count} tracks")

# Filter the DataFrame for that day
top_day_df = spotify_df[spotify_df['date'] == top_day]

# Display track and artist names
most_listened_tracks = top_day_df[['trackName', 'artistName']]

print("\n🎶 Tracks and Artists you listened to the most on that day:\n")
print(most_listened_tracks)


# %%
# Convert genre column to string safely
spotify_df['genre'] = spotify_df['genre'].astype(str)

# Now filter for Afrobeat
afrobeat_songs = spotify_df[spotify_df['genre'].str.lower().str.contains('afrobeats')]

# Group and count plays
top_afrobeat = (
    afrobeat_songs
    .groupby(['trackName', 'artistName'])
    .size()
    .reset_index(name='play_count')
    .sort_values(by='play_count', ascending=False)
)

print("🔥 Most Listened Afrobeat Songs:")
print(top_afrobeat.head(10))


# %%
# Ensure endTime is datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for late night hours (00:00 - 05:00)
late_night_df = spotify_df[spotify_df['hour'].between(0, 5)]

# Group by track and sum msPlayed
top_late_night_tracks = (
    late_night_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_late_night_tracks['Minutes Listened'] = top_late_night_tracks['msPlayed'] / (1000 * 60)

# Display results
print(top_late_night_tracks[['trackName', 'artistName', 'Minutes Listened']])


# %%
# Make sure endTime is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for evening (17:00 to 21:00)
evening_df = spotify_df[spotify_df['hour'].between(17, 21)]

# Group by track and artist, sum msPlayed
top_evening_tracks = (
    evening_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_evening_tracks['Minutes Listened'] = top_evening_tracks['msPlayed'] / (1000 * 60)

# Show result
print(top_evening_tracks[['trackName', 'artistName', 'Minutes Listened']])

# %%
# Ensure 'endTime' is datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract the hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for morning hours (6 AM to 11:59 AM)
morning_df = spotify_df[spotify_df['hour'].between(6, 11)]

# Group by track and artist, sum msPlayed
top_morning_tracks = (
    morning_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_morning_tracks['Minutes Listened'] = top_morning_tracks['msPlayed'] / (1000 * 60)

# Show result
print(top_morning_tracks[['trackName', 'artistName', 'Minutes Listened']])


# %%
# Ensure 'endTime' is datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract the hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for afternoon hours (12 PM to 5:59 PM)
afternoon_df = spotify_df[spotify_df['hour'].between(12, 17)]

# Group by track and artist, sum msPlayed
top_afternoon_tracks = (
    afternoon_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_afternoon_tracks['Minutes Listened'] = top_afternoon_tracks['msPlayed'] / (1000 * 60)

# Display result
print(top_afternoon_tracks[['trackName', 'artistName', 'Minutes Listened']])


# %%
# Ensure 'endTime' is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for night hours (20:00 - 23:59)
night_df = spotify_df[spotify_df['hour'].between(20, 23)]

# Group by track and artist, sum msPlayed
top_night_tracks = (
    night_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_night_tracks['Minutes Listened'] = top_night_tracks['msPlayed'] / (1000 * 60)

# Show results
print(top_night_tracks[['trackName', 'artistName', 'Minutes Listened']])


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.barplot(
    data=genre_playtime.head(15),  # top 15 for readability
    y='genre',
    x='Hours Listened',
    palette='magma'
)

plt.title("🎧 Listening Time per Genre", fontsize=16)
plt.xlabel("Hours Listened")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_lullabies,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    palette='Purples_d',
    dodge=False
)

plt.title("💤 Top 5 Lullaby Songs You Listened To", fontsize=14)
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title="Artist", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Convert endTime to datetime format if not already
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract hour from endTime
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Group by hour and sum msPlayed
hourly_listening = (
    spotify_df.groupby('hour')['msPlayed']
    .sum()
    .reset_index()
)

# Convert msPlayed to hours for readability
hourly_listening['Hours Listened'] = hourly_listening['msPlayed'] / (1000 * 60 * 60)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=hourly_listening, x='hour', y='Hours Listened', palette='viridis')

plt.title("🎶 Listening Time by Hour of Day", fontsize=14)
plt.xlabel("Hour of Day (24-hour format)")
plt.ylabel("Hours Listened")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_late_night_tracks,
    y='trackName',
    x='Minutes Listened',
    hue='artistName',
    dodge=False,
    palette='magma'
)

plt.title("🌙 Top 5 Most Listened Songs (Late Night: 12AM–5AM)")
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title='Artist', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_evening_tracks,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    dodge=False,
    palette='viridis'
)

plt.title("🎧 Top 5 Songs You Listened to Most in the Evening (17:00–21:00)")
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title='Artist', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_morning_tracks,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    palette='YlGnBu',
    dodge=False
)

plt.title("☀️ Top 5 Songs You Listened to Most in the Morning (6–11 AM)", fontsize=14)
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title="Artist", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_afternoon_tracks,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    palette='Oranges',
    dodge=False
)

plt.title("🌞 Top 5 Songs You Listened to in the Afternoon (12–5 PM)", fontsize=14)
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title="Artist", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_night_tracks,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    palette='Purples',
    dodge=False
)

plt.title("🌙 Top 5 Songs You Listened to at Night (8PM–12AM)", fontsize=14)
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title="Artist", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
import pandas as pd

# Make sure timestamp is datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract the hour
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter early morning (5AM to 8AM)
early_df = spotify_df[(spotify_df['hour'] >= 5) & (spotify_df['hour'] < 8)]

# Group by track and artist, sum time
top_early_tracks = (
    early_df.groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
)

# Convert to minutes
top_early_tracks['Minutes Listened'] = top_early_tracks['msPlayed'] / (1000 * 60)

# Get top 5
top_early_tracks = top_early_tracks.sort_values(by='Minutes Listened', ascending=False).head(5)


# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_early_tracks,
    x='Minutes Listened',
    y='trackName',
    hue='artistName',
    palette='Blues_d',
    dodge=False
)

plt.title("🌄 Top 5 Songs You Listened to in Early Morning (5AM–8AM)", fontsize=14)
plt.xlabel("Minutes Listened")
plt.ylabel("Track Name")
plt.legend(title="Artist", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure 'date' column is datetime
spotify_df['date'] = pd.to_datetime(spotify_df['date'])

# Extract weekday name (e.g., Monday, Tuesday)
spotify_df['weekday'] = spotify_df['date'].dt.day_name()

# Group by weekday and sum up msPlayed
weekday_time = (
    spotify_df.groupby('weekday')['msPlayed']
    .sum()
    .reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])  # ordered
    .reset_index()
)

# Convert msPlayed to hours for better readability (optional)
weekday_time['Hours Listened'] = weekday_time['msPlayed'] / (1000 * 60 * 60)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=weekday_time, x='weekday', y='Hours Listened', palette='magma')

plt.title("🎧 Listening Time by Day of the Week", fontsize=14)
plt.xlabel("Day of the Week")
plt.ylabel("Hours Listened")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# Ensure timestamp column is datetime
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'], errors='coerce')

# Extract month name
spotify_df['month'] = spotify_df['endTime'].dt.month_name()

# Now filter for September
september_tracks = spotify_df[spotify_df['month'].str.lower() == 'september']

# Group by track name and sum msPlayed
top_5_tracks_september = (
    september_tracks.groupby('trackName')['msPlayed']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# Rename columns
top_5_tracks_september.columns = ['Track Name', 'Total msPlayed']

# Display
print(top_5_tracks_september)


# %%
# Ensure endTime is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract hour if not already done
spotify_df['hour'] = spotify_df['endTime'].dt.hour

# Filter for early morning (5AM–7:59AM)
early_morning_df = spotify_df[spotify_df['hour'].between(5, 7)]

# Group by track and artist, sum msPlayed
top_early_tracks = (
    early_morning_df
    .groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(5)
)

# Convert msPlayed to minutes
top_early_tracks['Minutes Listened'] = top_early_tracks['msPlayed'] / (1000 * 60)

# Display results
print(top_early_tracks[['trackName', 'artistName', 'Minutes Listened']])


# %%
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_5_tracks_september,
    y='Track Name',
    x='Total msPlayed',
    palette='magma'
)

plt.title("🎧 Top 5 Tracks by Listening Time in September", fontsize=14)
plt.xlabel("Total Listening Time (ms)")
plt.ylabel("Track Name")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Group by artist and sum the total listening time
top_artists_time = (
    spotify_df.groupby('artistName')['msPlayed']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# Convert msPlayed to hours or minutes if you'd like
top_artists_time['Minutes Played'] = (top_artists_time['msPlayed'] / 60000).round(2)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_artists_time,
    x='Minutes Played',
    y='artistName',
    palette='rocket'
)

plt.title("🎧 Top 5 Most Listened Artists (by Total Listening Time)", fontsize=14)
plt.xlabel("Total Listening Time (Minutes)")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter for summer season
summer_df = spotify_df[spotify_df['season'].str.lower() == 'summer']

# Group by track and artist, sum msPlayed
top_summer_tracks = (
    summer_df.groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(3)
)

# Combine track and artist for clearer labels
top_summer_tracks['label'] = top_summer_tracks['trackName'] + " - " + top_summer_tracks['artistName']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_summer_tracks,
    y='label',
    x='msPlayed',
    palette='summer'
)

plt.title("☀️ Top 3 Most Listened Songs in Summer", fontsize=14)
plt.xlabel("Milliseconds Played")
plt.ylabel("Track - Artist")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter for summer season
winter_df = spotify_df[spotify_df['season'].str.lower() == 'winter']

# Group by track and artist, sum msPlayed
top_winter_tracks = (
    winter_df.groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(3)
)

# Combine track and artist for clearer labels
top_winter_tracks['label'] = top_winter_tracks['trackName'] + " - " + top_winter_tracks['artistName']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_winter_tracks,
    y='label',
    x='msPlayed',
    palette='winter'
)

plt.title("☀️ Top 3 Most Listened Songs in Winter", fontsize=14)
plt.xlabel("Milliseconds Played")
plt.ylabel("Track - Artist")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter for summer season
spring_df = spotify_df[spotify_df['season'].str.lower() == 'spring']

# Group by track and artist, sum msPlayed
top_spring_tracks = (
    spring_df.groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(3)
)

# Combine track and artist for clearer labels
top_spring_tracks['label'] = top_spring_tracks['trackName'] + " - " + top_spring_tracks['artistName']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_spring_tracks,
    y='label',
    x='msPlayed',
    palette='spring'
)

plt.title("☀️ Top 3 Most Listened Songs in Spring", fontsize=14)
plt.xlabel("Milliseconds Played")
plt.ylabel("Track - Artist")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Filter for summer season
autumn_df = spotify_df[spotify_df['season'].str.lower() == 'autumn']

# Group by track and artist, sum msPlayed
top_autumn_tracks = (
    autumn_df.groupby(['trackName', 'artistName'])['msPlayed']
    .sum()
    .reset_index()
    .sort_values(by='msPlayed', ascending=False)
    .head(3)
)

# Combine track and artist for clearer labels
top_autumn_tracks['label'] = top_autumn_tracks['trackName'] + " - " + top_autumn_tracks['artistName']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_summer_tracks,
    y='label',
    x='msPlayed',
    palette='autumn'
)

plt.title("☀️ Top 3 Most Listened Songs in Autumn", fontsize=14)
plt.xlabel("Milliseconds Played")
plt.ylabel("Track - Artist")
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt

# Ensure endTime is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract month name
spotify_df['month'] = spotify_df['endTime'].dt.month_name()

# Count number of tracks per month
monthly_counts = spotify_df['month'].value_counts().sort_index()

# Display the month you listened the most
most_listened_month = monthly_counts.idxmax()
most_listened_count = monthly_counts.max()

print(f"🎶 You listened to the most music in **{most_listened_month}** with {most_listened_count} tracks!")

# Optional: Plot
plt.figure(figsize=(10, 6))
monthly_counts.plot(kind='bar', color='skyblue')
plt.title("Monthly Music Listening Frequency 🎧")
plt.xlabel("Month")
plt.ylabel("Number of Tracks Played")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt

# Make sure endTime is in datetime format
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract date only (no time)
spotify_df['date'] = spotify_df['endTime'].dt.date

# Count tracks played per date
daily_counts = spotify_df['date'].value_counts().sort_index()

# Get the most active day
top_day = daily_counts.idxmax()
top_day_count = daily_counts.max()

print(f"📅 You listened to the most music on **{top_day}** with {top_day_count} tracks!")

# Optional: Plot top 10 most active days
top_10_days = daily_counts.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_10_days.plot(kind='bar', color='orchid')
plt.title("Top 10 Most Active Music Listening Days")
plt.xlabel("Date")
plt.ylabel("Tracks Played")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# Convert endTime to datetime if it isn't already
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract the date
spotify_df['date'] = spotify_df['endTime'].dt.date

# Find the day with the most listening activity
most_active_day = df['date'].value_counts().idxmax()
print("📅 Most active listening day:", most_active_day)


# %%
# Convert endTime to datetime if it isn't already
spotify_df['endTime'] = pd.to_datetime(spotify_df['endTime'])

# Extract the date
spotify_df['date'] = spotify_df['endTime'].dt.date

# Find the day with the most listening activity
most_active_day = spotify_df['date'].value_counts().idxmax()
print("📅 Most active listening day:", most_active_day)


# Filter songs played on the most active day
top_day_df = spotify_df[spotify_df['date'] == most_active_day]

# Group by track and artist, count plays
most_played_tracks = (
    top_day_df
    .groupby(['trackName', 'artistName'])
    .size()
    .reset_index(name='play_count')
    .sort_values(by='play_count', ascending=False)
)

print("🎶 Top songs and artists on that day:")
print(most_played_tracks.head(5))

# Plot bar chart of top played tracks
plt.figure(figsize=(12, 6))
sns.barplot(
    data=most_played_tracks.head(5),
    x='play_count',
    y='trackName',
    hue='artistName',
    dodge=False,
    palette='muted'
)

plt.title(f"🎵 Most Played Songs on {most_active_day}")
plt.xlabel("Play Count")
plt.ylabel("Track Name")
plt.legend(title='Artist', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



# %% [markdown]
# # Location API

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


# %%
# Assuming the 'date' column exists in the format 'YYYY-MM-DD' or similar
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])  # Convert to datetime if not already
weather_df['month'] = weather_df['datetime'].dt.month_name()  # Extract the month name

# Check the new 'month' column
print(weather_df.head())


# %% [markdown]
# # Converting AI Output to DataFrame 



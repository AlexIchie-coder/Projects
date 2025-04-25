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

# Assuming the 'date' column exists in the format 'YYYY-MM-DD' or similar
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])  # Convert to datetime if not already
weather_df['month'] = weather_df['datetime'].dt.month_name()  # Extract the month name

# Check the new 'month' column
print(weather_df.head())


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
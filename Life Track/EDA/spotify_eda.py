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
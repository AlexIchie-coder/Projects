import os
from dotenv import load_dotenv
import psycopg
import datetime as dt

load_dotenv()

DBCONN = os.getenv("DBCONN")

def save_day(data):
    conn = psycopg.connect(DBCONN)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS daily_log (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            location TEXT,
            activity TEXT,
            songs JSONB,
            genres JSONB,
            weather TEXT,
            people JSONB,
            mood TEXT,
            day_summary TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    ''')

    cur.execute('''
        INSERT INTO daily_log (date, location, activity, songs, genres, weather, people, mood, day_summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date, location) DO NOTHING;
    ''', (
        data['date'],
        data['location'],
        data['activity'],
        data['songs'],
        data['genres'],
        data['weather'],
        data['people'],
        data['mood'],
        data['day_summary']
    ))

    conn.commit()
    cur.close()
    conn.close()

# 📔 AI Diary Dashboard - Streamlit App

import streamlit as st
import pandas as pd
from datetime import datetime

# ---- SETTINGS ----
csv_filename = "diary_entries.csv"  # or "diary_entries_20240427_1542.csv" (match your file name)

# ---- LOAD DATA ----
@st.cache_data
def load_diary_entries(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is datetime
    return df

df_diary = load_diary_entries(csv_filename)

# ---- SIDEBAR ----
st.sidebar.title("📖 Diary Filters")
selected_label = st.sidebar.selectbox(
    "Choose Diary Type",
    options=["All"] + sorted(df_diary['Label'].unique())
)

# ---- MAIN PAGE ----
st.title("🪄 AI Diary Entries Dashboard")
st.caption("Generated with Gemini AI ✨")

# Filter by selected Label
if selected_label != "All":
    filtered_diary = df_diary[df_diary['Label'] == selected_label]
else:
    filtered_diary = df_diary

# Sort entries (most recent first)
filtered_diary = filtered_diary.sort_values(by="Date", ascending=False)

# Display entries
for idx, row in filtered_diary.iterrows():
    with st.expander(f"📅 {row['Date'].strftime('%Y-%m-%d')} | 🏷️ {row['Label']}"):
        st.markdown(row['DiaryEntry'])

# ---- FOOTER ----
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Gemini AI, and Python")


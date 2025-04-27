import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- Page Configuration
st.set_page_config(page_title="ICHIE DIARY", layout="wide")

# --- Load Modules
from eda.weather_eda import show_weather_dashboard, load_weather_data
from eda.spotify_eda import show_spotify_dashboard, load_spotify_data

# --- Load Data
diary_df = pd.read_csv("diary_entries.csv", parse_dates=["Date"])
weather_df = load_weather_data()
spotify_df = load_spotify_data()

# --- Title
st.title("📚 Life Track Dashboard")

# --- Tabs Navigation
tabs = st.tabs(["🌦️ Weather", "🎶 Spotify", "📔 Diary"])

# --- Weather Dashboard
with tabs[0]:
    show_weather_dashboard(weather_df)

# --- Spotify Dashboard
with tabs[1]:
    show_spotify_dashboard(spotify_df)

# --- Diary Dashboard
with tabs[2]:

    diary_df_sorted = diary_df.sort_values(by="Date", ascending=False)

    # --- Filter by Label
    st.subheader("🔎 Filter Diary")

    selected_label = st.selectbox(
        "Choose an entries:",
        options=["Day"] + sorted(diary_df_sorted["Label"].unique())
    )

    if selected_label != "All":
        filtered_diary = diary_df_sorted[diary_df_sorted["Label"] == selected_label]
    else:
        filtered_diary = diary_df_sorted

    # --- Calendar View
    st.subheader("🗓️ Calendar View")

    selected_date = st.date_input(
        "Pick a date to view the diary entry:",
        value=filtered_diary["Date"].max().date()
    )

    diary_on_date = filtered_diary[filtered_diary["Date"].dt.date == selected_date]

    if not diary_on_date.empty:
        for idx, row in diary_on_date.iterrows():
            st.markdown(f"### 📅 {row['Date'].strftime('%Y-%m-%d')} | 🏷️ {row['Label']}")
            st.markdown(row['DiaryEntry'])
    else:
        st.info("No diary entry for this date.")

    st.markdown("---")

    # --- Full Diary List
    st.subheader("📚 Full Diary List")

    for idx, row in filtered_diary.iterrows():
        with st.expander(f"📅 {row['Date'].strftime('%Y-%m-%d')} | 🏷️ {row['Label']}"):
            st.markdown(row['DiaryEntry'])

    st.markdown("---")

    # --- Download Section
    st.subheader("⬇️ Download Your Diary Entries")

    # Prepare diary text
    diary_text = ""
    for idx, row in filtered_diary.iterrows():
        diary_text += f"Date: {row['Date'].strftime('%Y-%m-%d')}\n"
        diary_text += f"Label: {row['Label']}\n"
        diary_text += f"Entry:\n{row['DiaryEntry']}\n"
        diary_text += "-" * 50 + "\n\n"

    # --- TXT Download
    st.download_button(
        label="📄 Download as TXT",
        data=diary_text,
        file_name="diary_entries.txt",
        mime="text/plain"
    )

    # --- PDF Download
    def save_diary_as_pdf(diary_df):
        pdf = FPDF()
        pdf.add_page()

        font_path = "DejaVuSans.ttf"  # Ensure you have this font in your folder
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)

        for index, row in diary_df.iterrows():
            date = row["Date"].strftime("%Y-%m-%d")
            label = row["Label"]
            entry = row["DiaryEntry"]

            pdf.cell(0, 10, f"{date} - {label}", ln=True)
            pdf.multi_cell(0, 10, entry)
            pdf.ln(5)

        return pdf.output(dest='S').encode('latin1')

    if st.button("📄 Download Diary as PDF"):
        pdf_bytes = save_diary_as_pdf(filtered_diary)
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name="diary_entries.pdf",
            mime="application/pdf"
        )

    st.caption("Powered by EBUKA ✨")

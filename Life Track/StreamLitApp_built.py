import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
from functools import lru_cache
import streamlit_authenticator as stauth



# --- Page Configuration
st.set_page_config(page_title="ICHIE DIARY", layout="wide")

# --- 🛠 FIRST initialize session states ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "mode" not in st.session_state:
    st.session_state.mode = "Login"
if "users" not in st.session_state:
    st.session_state.users = {
        "ichie": {"email": "ichie@example.com", "password": "yourpassword"},
        "admin": {"email": "admin@example.com", "password": "adminpass"},
    }

# --- Initialize Session States ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "mode" not in st.session_state:
    st.session_state.mode = "Login"  # or "Signup"

# --- Authentication Logic ---
def login():
    st.markdown(
        """
        <div style='
            padding: 40px;
            background: linear-gradient(135deg, #f5f5dc, #f0e6d2);
            border-radius: 15px;
            box-shadow: inset 0 0 10px rgba(139,69,19,0.15), 0 8px 25px rgba(0,0,0,0.15);
            margin: 30px;
            border: 1.5px solid #d2b48c;
            background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
            background-blend-mode: multiply;
        '>
            <h1 style='
                text-align: center;
                font-size: 48px;
                color: #5c4033;
                font-family: Georgia, serif;
                text-shadow: 1px 1px 2px #deb887;
            '>🔒 Login to Ichie's Diary</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username", key="login_username")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["email"] == email and user["password"] == password:
            st.session_state.authenticated = True
            st.success("Login successful! 🎉")
            st.rerun()
        else:
            st.error("Invalid login details. Please try again.")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.mode = "Signup"
        st.rerun()


def signup():
    st.markdown(
        """
        <div style='
            padding: 40px;
            background: linear-gradient(135deg, #f5f5dc, #f0e6d2);
            border-radius: 15px;
            box-shadow: inset 0 0 10px rgba(139,69,19,0.15), 0 8px 25px rgba(0,0,0,0.15);
            margin: 30px;
            border: 1.5px solid #d2b48c;
            background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
            background-blend-mode: multiply;
        '>
            <h1 style='
                text-align: center;
                font-size: 48px;
                color: #5c4033;
                font-family: Georgia, serif;
                text-shadow: 1px 1px 2px #deb887;
            '>📝 Sign Up for Ichie's Diary</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    new_username = st.text_input("Choose a Username", key="signup_username")
    new_email = st.text_input("Enter your Email", key="signup_email")
    new_password = st.text_input("Create a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if new_username in st.session_state.users:
            st.error("Username already exists. Please choose another.")
        else:
            st.session_state.users[new_username] = {"email": new_email, "password": new_password}
            st.success("Account created successfully! Please log in.")
            st.session_state.mode = "Login"
            st.rerun()

    if st.button("Already have an account? Login"):
        st.session_state.mode = "Login"
        st.rerun()


# --- Main App Logic ---
if not st.session_state.authenticated:
    if st.session_state.mode == "Login":
        login()
    elif st.session_state.mode == "Signup":
        signup()
    st.stop()

# --- After Successful Login ---
st.success(f"Welcome, {st.session_state.get('login_username', 'User')}! 🎉")



# --- Load Modules
from eda.weather_eda import show_weather_dashboard, load_weather_data
from eda.spotify_eda import show_spotify_dashboard, load_spotify_data

# --- Load Data
diary_df = pd.read_csv("diary_entries.csv", parse_dates=["Date"])
weather_df = load_weather_data()
spotify_df = load_spotify_data()

# --- Sort Diary
diary_df_sorted = diary_df.sort_values(by="Date", ascending=False)


# --- Tabs Navigation with Shiny and Colorful Style
st.markdown("""
    <style>
    /* Make the tab headers colorful and shiny */
    [data-testid="stTabs"] button {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        border: 2px solid #8b5a2b;
        border-radius: 12px;
        padding: 10px 20px;
        margin: 5px;
        color: #5c4033;
        font-weight: bold;
        font-family: Georgia, serif;
        font-size: 18px;
        text-shadow: 1px 1px 2px #fff5e1;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(222,184,135,0.8);
    }
    [data-testid="stTabs"] button:hover {
        background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
        color: #5c4033;
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(210,180,140,0.9);
    }
    [data-testid="stTabs"] button:focus {
        background: linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%);
        color: #5c4033;
        border: 2px solid #5c4033;
    }
    </style>
""", unsafe_allow_html=True)

tabs = st.tabs(["🏠 HOME", "🌦️ WEATHER", "🎶 SPOTIFY",  "📔 DIARY"])


# --- Home Dashboard
with tabs[0]:
    st.markdown(
    """
    <div style='
        text-align: center;
        padding: 60px;
        background: linear-gradient(135deg, #f5f5dc, #f0e6d2);
        border-radius: 15px;
        box-shadow: inset 0 0 10px rgba(139,69,19,0.2), 0 8px 25px rgba(0,0,0,0.2);
        margin: 30px;
        border: 1.5px solid #d2b48c;
        background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
        background-blend-mode: multiply;
    '>
        <h1 style='
            font-size: 80px;
            color: #5c4033;
            font-family: "Georgia", serif;
            text-shadow: 1px 1px 2px #deb887;
            margin-bottom: 10px;
        '>
            📜✨ ICHIE'S DIARY ✨📜
        </h1>
        <p style='
            font-size: 24px;
            color: #8b5a2b;
            font-family: Georgia, serif;
            margin-top: 20px;
            text-shadow: 0.5px 0.5px 1px #d2b48c;
        '>
            Welcome to your timeless life scroll... 🌟🕰️
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Weather Dashboard
with tabs[1]:
    show_weather_dashboard(weather_df)

# --- Spotify Dashboard
with tabs[2]:
    show_spotify_dashboard(spotify_df)

# --- Caching Mood API Calls
@lru_cache(maxsize=1000)
def detect_mood(text):
    url = "https://ekman-emotion-analysis.p.rapidapi.com/ekman-emotion"
    payload = [{"id": "1", "language": "en", "text": text}]
    headers = {
        "x-rapidapi-key": "X-Rapidapi-Key",  # <-- Put your correct RapidAPI Key
        "x-rapidapi-host": "ekman-emotion-analysis.p.rapidapi.com",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(result[0])
            if isinstance(result, list) and 'predictions' in result[0]:
                mood = result[0]['predictions'][0]['prediction']
                return mood.capitalize()
            else:
                st.warning(f"No emotion detected by API. Full response: {result}")
                return smart_guess_mood(text)  # fallback if emotion missing
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return smart_guess_mood(text)
    except Exception as e:
        st.warning(f"Error contacting Mood API: {str(e)}")
        return smart_guess_mood(text)

# --- Smart Guess Mood fallback (simple keyword analysis)
def smart_guess_mood(text):
    text = text.lower()
    if any(word in text for word in ["happy", "joy", "love", "excited", "great", "good"]):
        return "Happy"
    elif any(word in text for word in ["sad", "cry", "depressed", "unhappy"]):
        return "Sad"
    elif any(word in text for word in ["angry", "mad", "furious", "upset"]):
        return "Angry"
    elif any(word in text for word in ["calm", "relaxed", "peaceful"]):
        return "Calm"
    elif any(word in text for word in ["fear", "scared", "afraid", "nervous"]):
        return "Fearful"
    else:
        return "Neutral"

# --- Diary Dashboard
with tabs[3]:
    st.markdown("""
    <h1 style='
        font-family: Georgia, serif;
        background: linear-gradient(90deg, #d2b48c, #f5deb3);
        color: #5c4033;
        padding: 10px 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(139,69,19,0.4);
        display: inline-block;
    '>📔 AI Diary Dashboard</h1>
    """, unsafe_allow_html=True)

    # --- Filter by Label
    st.markdown("""
    <h2 style='
        font-family: Georgia, serif;
        color: #5c4033;
        background: linear-gradient(90deg, #d2b48c, #f5deb3);
        padding: 8px 15px;
        border-radius: 8px;
        box-shadow: 0px 2px 8px rgba(139,69,19,0.4);
        display: inline-block;
    '>🔎 Filter Diary by Label</h2>
    """, unsafe_allow_html=True)

    selected_label = st.selectbox(
        "Choose a label to filter entries:",
        options=["Day"] + sorted(diary_df_sorted["Label"].unique())
    )

    if selected_label != "All":
        filtered_diary = diary_df_sorted[diary_df_sorted["Label"] == selected_label]
    else:
        filtered_diary = diary_df_sorted

    import datetime

# # --- Calendar View
#     st.markdown("""
#     <h2 style='
#         font-family: Georgia, serif;
#         color: #5c4033;
#         background: linear-gradient(90deg, #d2b48c, #f5deb3);
#         padding: 8px 15px;
#         border-radius: 8px;
#         box-shadow: 0px 2px 8px rgba(139,69,19,0.4);
#         display: inline-block;
#     '>🗓️ Calendar View</h2>
#     """, unsafe_allow_html=True)

#     # Set date range: start from Jan 1, 2023 to today
#     min_date = datetime.date(2023, 1, 1)
#     max_date = datetime.date.today()

#     selected_date = st.date_input(
#         "Pick a date to view the diary entry:",
#         value=min(max_date, filtered_diary["Date"].max().date()),  # default date is last diary date or today
#         min_value=min_date,
#         max_value=max_date
#     )

#     diary_on_date = filtered_diary[filtered_diary["Date"].dt.date == selected_date]

#     if not diary_on_date.empty:
#         for idx, row in diary_on_date.iterrows():
#             mood = detect_mood(row['DiaryEntry'])
#             st.markdown(
#                 f"""
#                 <div style='
#                     background-image: url("https://images.unsplash.com/photo-1607082349250-559b147b95bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60");
#                     background-size: cover;
#                     background-repeat: no-repeat;
#                     background-position: center;
#                     padding: 30px;
#                     color: #5c4033;
#                     font-family: Georgia, serif;
#                     font-size: 18px;
#                     line-height: 1.6;
#                     border-radius: 20px;
#                     box-shadow: inset 0 0 30px rgba(139,69,19,0.5), 0 0 15px rgba(222,184,135,0.7);
#                     backdrop-filter: blur(2px);
#                 '>
#                     <b>Mood:</b> {mood}<br><br>
#                     {row['DiaryEntry']}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#     else:
#         st.info("No diary entry for this date.")

#     st.markdown("---")

    # --- Full Diary List
    st.markdown("""
    <h2 style='
        font-family: Georgia, serif;
        color: #5c4033;
        background: linear-gradient(90deg, #d2b48c, #f5deb3);
        padding: 10px 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(139,69,19,0.4);
        display: inline-block;
    '>📚 Full Diary List</h2>
    """, unsafe_allow_html=True)

    for idx, row in filtered_diary.iterrows():
        mood = detect_mood(row['DiaryEntry'])
        with st.expander(f"📅 {row['Date'].strftime('%Y-%m-%d')} | 🏷️ {row['Label']} | Mood: {mood}"):
            st.markdown(
                f"""
                <div style='
                    background-image: url("https://images.unsplash.com/photo-1607082349250-559b147b95bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                    padding: 30px;
                    color: #5c4033;
                    font-family: Georgia, serif;
                    font-size: 18px;
                    line-height: 1.6;
                    border-radius: 20px;
                    box-shadow: inset 0 0 30px rgba(139,69,19,0.5), 0 0 15px rgba(222,184,135,0.7);
                    backdrop-filter: blur(2px);
                '>
                    {row['DiaryEntry']}
                </div>
                """,
                unsafe_allow_html=True
            )

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

    def save_diary_as_pdf(diary_df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for index, row in diary_df.iterrows():
            date = row["Date"].strftime("%Y-%m-%d") if pd.notna(row["Date"]) else "Unknown Date"
            label = row.get("Label", "No Label")
            entry = row.get("DiaryEntry", "")

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
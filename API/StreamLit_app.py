import streamlit as st  
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
import psycopg

load_dotenv()

def get_data(curr):
    print("getting data for ", curr)
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute('''
        SELECT * FROM crypto where symbol = %s;
    ''', (curr,))

    Crypto_data =  cur.fetchall()
    cur.close()
    conn.close()

    crypto_data= pd.DataFrame(Crypto_data, columns = ['date','symbol','open','high','low','close','volume'])
    return crypto_data



st.title("CRYPTO MARKET UPDATES")
st.title("Digital Currency is :gold[cool] :money_with_wings:")

st.divider()

currency = st.selectbox(
    "Select Crypto Currency",
    ("BTC", "ETH", "SOL"),
)

crypto_data = get_data(currency)

st.write('You selected', currency)




# # Load your dataset
# #@st.cache_data  # Cache the data for better performance
# def load_data():
#     return pd.read_csv('Combined_Crypto_Data.csv')  # Make sure the file is in your working directory



# # Load the data
# crypto_data = load_data()

crypto_data['date'] = pd.to_datetime(crypto_data['date'])

# # Display the raw data if needed
# st.write("Raw Crypto Data Preview:")
# st.dataframe(crypto_data.head())

# # Create line chart with your actual data
st.subheader("Crypto Market Trends")
st.line_chart(crypto_data, x="date", y="open")  # Adjust columns to match your dataset

# # Alternative: If you want to keep the original structure but with your data
# if len(crypto_data) >= 20:
#     chart_data = crypto_data[['open', 'high', 'currency_name']].head(20)  # Get first 20 rows
#     chart_data.columns = ["a", "b", "c"]  # Rename columns to match original example
#     st.line_chart(chart_data)
# else:
#     st.warning("Not enough data points (need at least 20 rows)")


# Function to fetch crypto news from PostgreSQL
def get_crypto_news():
    try:
        dbconn = os.getenv("DBCONN")  # Get DB connection string from environment variable
        if not dbconn:
            st.error("Database connection string not found.")
            return pd.DataFrame()

        conn = psycopg.connect(dbconn)
        cur = conn.cursor()

        # Query to fetch crypto news
        query = "SELECT date, title, currency FROM crypto_news ORDER BY date DESC;"
        df = pd.read_sql(query, conn)

        cur.close()
        conn.close()
        return df

    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

# Streamlit App
def main():
    st.title("📈 Crypto News Dashboard")

    # Fetch data from PostgreSQL
    news_df = get_crypto_news()

    if news_df.empty:
        st.warning("⚠️ No news data found. Check your database connection.")
    else:
        # Display news in a table
        st.subheader("📰 Latest Crypto News")
        st.dataframe(news_df)

        # Display news as a list
        st.subheader("📅 News Highlights")
        for _, row in news_df.iterrows():
            st.write(f"📆 {row['date'].strftime('%Y-%m-%d')} | 📰 **{row['title']}** ({row['currency']})")

# Run the Streamlit App
if __name__ == "__main__":
    main()



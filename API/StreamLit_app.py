import streamlit as st  
from dotenv import load_dotenv
import os
import psycopg
import pandas as pd

st.title("CRYPTO MARKET UPDATES")
st.title("Digital Currency is :gold[cool] :money_with_wings:")

st.divider()

currency = st.selectbox(
    "Select Crypto Currency",
    ("Bitcoin", "Ethereum", "Solana"),
)

st.write('You selected', currency)



load_dotenv()

def get_api_data():
  dbconn = os.getenv("DBCONN")
  conn = psycopg.connect(dbconn)
  cur = conn.cursor()

  cur.execute('''
    SELECT * FROM api_data;
  ''')
  data = cur.fetchall()

  conn.commit()
  cur.close()
  conn.close()

  return pd.DataFrame(data, columns=["date", "open", "close"])

api_data = get_api_data()


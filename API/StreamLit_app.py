import streamlit as st  
from dotenv import load_dotenv
import os
import pandas as pd
import psycopg
from datetime import datetime

load_dotenv()

def get_db_connection():
    """Establish database connection"""
    dbconn = os.getenv("DBCONN")
    return psycopg.connect(dbconn)

def get_crypto_data(currency, year=None):
    """Fetch cryptocurrency price data with optional year filter"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if year:
            query = '''
                SELECT * FROM crypto 
                WHERE symbol = %s 
                AND date >= %s 
                AND date <= %s
                ORDER BY date ASC;
            '''
            start_date = datetime(year, 1, 1).strftime('%Y-%m-%d')
            end_date = datetime(year, 12, 31).strftime('%Y-%m-%d')
            cur.execute(query, (currency, start_date, end_date))
        else:
            cur.execute('''
                SELECT * FROM crypto 
                WHERE symbol = %s 
                ORDER BY date DESC;
            ''', (currency,))

        crypto_data = cur.fetchall()
        cur.close()
        conn.close()

        if crypto_data:
            df = pd.DataFrame(crypto_data, columns=['date','symbol','open','high','low','close','volume'])
            df['date'] = pd.to_datetime(df['date'])
            return df
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error fetching crypto data: {e}")
        return pd.DataFrame()

def get_crypto_news(currency=None):
    """Fetch crypto news with optional currency filter"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if currency:
            cur.execute('''
                SELECT date, title, currency 
                FROM crypto_news 
                WHERE currency = %s
                ORDER BY date DESC
                LIMIT 100;
            ''', (currency,))
        else:
            cur.execute('''
                SELECT date, title, currency 
                FROM crypto_news 
                ORDER BY date DESC
                LIMIT 100;
            ''')

        news_data = cur.fetchall()
        cur.close()
        conn.close()

        if news_data:
            df = pd.DataFrame(news_data, columns=['date','title','currency'])
            df['date'] = pd.to_datetime(df['date'])
            return df
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return pd.DataFrame()

def display_news_by_currency():
    """Display news filtered by selected currency"""
    st.subheader("🔍 Filter News by Currency")
    
    # Currency selection for news
    news_currency = st.selectbox(
        "Select Currency for News",
        ("All", "Bitcoin", "Ethereum", "Solana"),
        key="news_currency"
    )
    
    # Get news based on selection
    if news_currency == "All":
        news_df = get_crypto_news()
        title = "All Crypto News"
    else:
        news_df = get_crypto_news(news_currency)
        title = f"{news_currency} News"
    
    if not news_df.empty:
        # Display as dataframe
        st.dataframe(
            news_df,
            column_config={
                "date": "Date",
                "title": "Headline",
                "currency": "Currency"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Display as expandable list
        with st.expander("View as List"):
            news_df['date'] = pd.to_datetime(news_df['date']).dt.date
            for _, row in news_df.iterrows():
                st.markdown(f"""
                **{row['date']}**  
                {row['title']}  
                *{row['currency']}*
                """)
                st.divider()
    else:
        st.warning("No news found for the selected currency")

def main():
    st.set_page_config(page_title="Crypto Dashboard", layout="wide")
    
    st.title("💰 Crypto Market Dashboard")
    st.markdown("Digital Currency is :gold[cool] :money_with_wings:")
    st.divider()
    
    # Sidebar for filters
    with st.sidebar:
        st.header("Filters")
        currency = st.selectbox(
            "Select Crypto Currency",
            ("BTC", "ETH", "SOL"),
            index=0
        )
        
        # Year selection for price data
        current_year = datetime.now().year
        selected_year = st.selectbox(
            "Select Year for Price Data",
            range(2024, current_year + 1),
            index=len(range(2024, current_year + 1)) - 1  # Default to current year
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This dashboard displays cryptocurrency market data and news.")
    
    # Main content - Price Data
    st.subheader(f"{currency} Price Data ({selected_year})")
    crypto_data = get_crypto_data(currency, selected_year)
    
    if not crypto_data.empty:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Filter data for the selected year
            yearly_data = crypto_data[
                (crypto_data['date'].dt.year == selected_year)
            ]
            
            if not yearly_data.empty:
                st.line_chart(yearly_data, x="date", y=["high", "low"])
            else:
                st.warning(f"No data available for {selected_year}")
        
        with col2:
            latest = crypto_data.iloc[0] if not crypto_data.empty else None
            if latest is not None:
                st.metric("Current Price", f"${latest['close']:,.2f}")
                st.markdown(f"""
                - **Open:** ${latest['open']:,.2f}
                - **High:** ${latest['high']:,.2f}
                - **Low:** ${latest['low']:,.2f}
                - **Volume:** {latest['volume']:,.0f}
                """)
            else:
                st.warning("No price data available")
    else:
        st.warning("No price data available for the selected currency")
    
    # News section
    st.divider()
    display_news_by_currency()

if __name__ == "__main__":
    main()
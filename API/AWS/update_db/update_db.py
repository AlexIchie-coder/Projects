import os
import psycopg
import datetime as dt



def update_db(event, context):
    crypto_data_list = event
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    for crypto_data in crypto_data_list:
        # Convert date string to datetime object
        date = dt.datetime.strptime(crypto_data[0], '%Y-%m-%d').date()
        
        cur.execute('''
            INSERT INTO crypto (date, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date, symbol) DO NOTHING;''',
            (date, crypto_data[1], crypto_data[2], 
             crypto_data[3], crypto_data[4], 
             crypto_data[5], crypto_data[6]))

    conn.commit()
    cur.close()
    conn.close()


update_db([
    ('2025-04-08', 'BTC', 72521.05, 72879.2, 72329.37, 72360.16, 6.97223075),
    ('2025-04-08', 'ETH', 1421.95, 1431.03, 1411.76, 1411.76, 111.79132496),
    ('2025-04-08', 'SOL', 97.99, 102.61, 97.45, 101.49, 11251.358)
])

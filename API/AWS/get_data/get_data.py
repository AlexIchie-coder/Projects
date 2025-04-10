import os
import requests

def get_data():
    symbols=["BTC", "ETH", "SOL"]
    market="EUR"
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("⚠️ API_KEY not found in environment variables.")
        return []

    all_records = []

    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={api_key}"
        response = requests.get(url)
        print(response.status_code)

        if not response.ok:
            print(f"⚠️ Error fetching {symbol}: {response.status_code}")
            continue

        data = response.json()

        if "Time Series (Digital Currency Daily)" not in data:
            print(f"⚠️ Unexpected response for {symbol}:")
            print(json.dumps(data, indent=2))
            return[]

        time_series = data["Time Series (Digital Currency Daily)"]
        date = max(time_series.keys())
        values= time_series[date]

    #     # Convert to list of records

        try:
            record = {
                "date": date,
                "currency": symbol,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": float(values["5. volume"])
            }
            all_records.append(record)
        except KeyError as e:
                print(f"⚠️ Missing key for {symbol} on {date}: {e}")
    print(all_records)
    values = []
    for record in all_records:
        current_record_values = []
        for value in record.values():
            current_record_values.append(value)
        values.append(current_record_values)
    print(values)
    return all_records

get_data()

# Example usage
#crypto_data = get_data()
#if crypto_data:
    #print(json.dumps(crypto_data[:3], indent=2))  # Preview first 3 entries
#else:
    #print("⚠️ No crypto data fetched.")

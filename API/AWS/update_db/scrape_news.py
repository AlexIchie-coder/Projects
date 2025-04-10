import requests
from datetime import datetime
import bs4
import pandas as pd

def scrape_news(currency):
    url = f"https://u.today/search/node?keys={currency}"
    response = requests.get(url, timeout=10)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    news_data = []
    for card in soup.select('div.news__item'):
        data = []
        date_element = card.select_one('div.news__item-head div.humble')
        if date_element:
            datestr = date_element.get_text().split(" - ")[0]
            try:
                data.append(datetime.strptime(datestr, "%b %d, %Y").date())
            except ValueError:
                continue  # Skip invalid dates
        
        title_element = card.select_one('div.news__item-title')
        if title_element:
            data.append(title_element.get_text())
        
        if len(data) == 2:
            news_data.append(tuple(data))
    
    df = pd.DataFrame(news_data, columns=['date', 'title'])
    df['currency'] = currency
    return df

def lambda_handler(event, context):
    currencies = ["Bitcoin", "Ethereum", "Solana"]
    all_data = pd.concat([scrape_news(currency) for currency in currencies])
    
    # Convert to dictionary for JSON response
    result = all_data.to_dict('records')
    
    return {
        'statusCode': 200,
        'body': result
    }
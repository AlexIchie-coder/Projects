import requests
from datetime import datetime
import bs4

def get_news_data(currency):
    url = f"https://u.today/search/node?keys={currency}"
    response = requests.get(url, timeout=10)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    news_data = []
    for card in soup.select('div.news__item'):
        data = {}
        date_element = card.select_one('div.news__item-head div.humble')
        if date_element:
            datestr = date_element.get_text().split(" - ")[0]
            try:
                data['date'] = datetime.strptime(datestr, "%b %d, %Y").date().isoformat()
            except ValueError:
                continue  # Skip invalid dates
        
        title_element = card.select_one('div.news__item-title')
        if title_element:
            data['title'] = title_element.get_text()
        
        if len(data) == 2:  # Both date and title present
            data['currency'] = currency
            news_data.append(data)
    
    return news_data

def lambda_handler(event, context):
    currencies = ["Bitcoin", "Ethereum", "Solana"]
    all_data = []
    
    for currency in currencies:
        currency_data = get_news_data(currency)
        all_data.extend(currency_data)
    
    return {
        'statusCode': 200,
        'body': all_data
    }


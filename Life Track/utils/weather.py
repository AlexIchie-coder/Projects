import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WeatherAPI")

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        desc = data['current']['condition']['text']
        temp = data['current']['temp_c']
        return f"{desc}, {temp}°C"
    else:
        return "Weather info unavailable"

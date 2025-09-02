import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment Variables:")
print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")
print(f"RAPIDAPI_KEY: {os.getenv('RAPIDAPI_KEY')}")
print(f"OPENWEATHER_API_KEY: {os.getenv('OPENWEATHER_API_KEY')}")

# Test OpenWeather API directly
import requests

api_key = os.getenv('OPENWEATHER_API_KEY')
if api_key:
    print(f"\nTesting OpenWeather API with key: {api_key}")
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Hyderabad",
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"API Response Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Temperature: {data['main']['temp']}°C")
            print("✅ OpenWeather API is working!")
        else:
            print(f"API Error: {response.text}")
    except Exception as e:
        print(f"API Request Error: {e}")
else:
    print("❌ No OpenWeather API key found")
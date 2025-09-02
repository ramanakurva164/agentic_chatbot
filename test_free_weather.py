import requests
import json

def test_free_weather_api(city="Hyderabad"):
    """Test the free wttr.in weather API"""
    try:
        url = f"http://wttr.in/{city}?format=j1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"🌐 Testing free weather API for {city}...")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
            description = current['weatherDesc'][0]['value']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            visibility = current['visibility']
            
            print("✅ Free weather API is working!")
            print(f"""🌤️ Weather for {city}:
📍 Location: {city}
🌡️ Temperature: {temp_c}°C ({temp_f}°F)
🌡️ Feels Like: {feels_like}°C
☁️ Condition: {description}
💨 Wind: {wind_speed} km/h {wind_dir}
💧 Humidity: {humidity}%
👁️ Visibility: {visibility} km""")
            
            return True
        else:
            print(f"❌ Free API failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Free API error: {e}")
        return False

if __name__ == "__main__":
    # Test multiple cities
    cities = ["Hyderabad", "Tandur", "Mumbai", "London"]
    
    for city in cities:
        print(f"\n{'='*50}")
        test_free_weather_api(city)
        print(f"{'='*50}")
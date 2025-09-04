import os
import requests
import math
import re
from datetime import datetime
import urllib.parse
import google.generativeai as genai
from dotenv import load_dotenv
import base64
from transformers import pipeline, AutoTokenizer
import streamlit as st

# Load environment variables at the module level
load_dotenv()



class NlpTool:
    def __init__(self):
        print("🧠 Initializing NLP Tool with Hugging Face models...")

        # Load Hugging Face pipelines
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
        self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

        print("✅ NLP Tool ready!")

    def handle_input(self, query: str):
        query_lower = query.lower()

        try:
            if query_lower.startswith("summarize"):
                text = query.replace("summarize", "", 1).strip()
                result = self.summarizer(text, max_length=100, min_length=20, do_sample=False)
                return result[0]['summary_text']

            elif query_lower.startswith("sentiment"):
                text = query.replace("sentiment", "", 1).strip()
                result = self.sentiment_analyzer(text)
                return f"Sentiment: {result[0]['label']} (score: {result[0]['score']:.2f})"

            elif query_lower.startswith("translate"):
                text = query.replace("translate", "", 1).strip()
                result = self.translator(text)
                return f"French Translation: {result[0]['translation_text']}"

            elif query_lower.startswith("entities") or query_lower.startswith("extract"):
                text = query.replace("entities", "", 1).replace("extract", "", 1).strip()
                result = self.ner(text)
                return [{"entity": r['entity_group'], "word": r['word'], "score": round(r['score'], 2)} for r in result]

            elif query_lower.startswith("tokenize"):
                text = query.replace("tokenize", "", 1).strip()
                tokens = self.tokenizer.tokenize(text)
                return tokens

            elif query_lower.startswith("keywords"):
                text = query.replace("keywords", "", 1).strip()
                # Very simple keyword extraction: top N tokens
                tokens = self.tokenizer.tokenize(text)
                keywords = list(set([t for t in tokens if t.isalpha()]))
                return keywords[:10]

            elif query_lower.startswith("paraphrase") or query_lower.startswith("nlp"):
                # For simplicity, reuse summarizer as paraphraser
                text = query.replace("paraphrase", "", 1).replace("nlp", "", 1).strip()
                result = self.summarizer(text, max_length=100, min_length=20, do_sample=True)
                return f"Paraphrased: {result[0]['summary_text']}"

            else:
                return "❌ NLPTool: Unknown NLP command. Try one of: summarize, sentiment, translate, extract, tokenize, entities, keywords, paraphrase."

        except Exception as e:
            return f"⚠️ NLPTool error: {str(e)}"



class ChatTool:
    def __init__(self):
        self.name = "ChatTool"
        self.model = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the Gemini model"""
        try:
            # Get API key from environment
            api_key = os.getenv("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY"))
            
            if not api_key:
                print("❌ GEMINI_API_KEY not found in environment variables")
                self.model = None
                return
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Try different model names (Google has updated their models)
            model_names = [
                'gemini-1.5-flash',
                'gemini-1.5-pro', 
                'gemini-1.0-pro',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro',
                'models/gemini-1.0-pro'
            ]
            
            for model_name in model_names:
                try:
                    print(f"🤖 Trying to load model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    
                    # Test the model with a simple query
                    test_response = self.model.generate_content("Hello")
                    if test_response and test_response.text:
                        print(f"✅ Successfully loaded model: {model_name}")
                        return
                        
                except Exception as e:
                    print(f"❌ Failed to load {model_name}: {e}")
                    continue
            
            print("❌ All model loading attempts failed")
            self.model = None
            
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            self.model = None
    
    def handle_input(self, query):
        """Handle general chat queries using Gemini"""
        try:
            if self.model is None:
                return """🤖 Gemini Chat Model Not Available

The Gemini API might be experiencing issues or the model names have changed.

**Try these solutions:**
1. Get a new API key from Google AI Studio (ai.google.dev)
2. Check if your API key has the correct permissions
3. The API might be temporarily down

**Meanwhile, I can still help you with:**
- 🌤️ Weather information (any city)
- 🔍 Web search (links to resources)  
- 🧮 Mathematical calculations
- 🔤 String operations

Try: "weather in your_city" or "calculate 2+2" """
            
            # Create a conversation prompt
            prompt = f"""You are a helpful AI assistant. Respond in a friendly and conversational manner.
            Keep your responses concise but informative.
            
            User: {query}
            Assistant:"""
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I'm having trouble generating a response right now. Could you try rephrasing your question?"
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if "404" in error_msg or "not found" in error_msg:
                return """🤖 Gemini Model Error

The Gemini model is not available. This usually means:
1. **API Key Issue**: Your API key might be invalid or expired
2. **Model Changed**: Google may have updated their model names
3. **Quota Exceeded**: You might have hit API limits

**Solutions:**
1. Get a new API key from [Google AI Studio](https://ai.google.dev)
2. Wait a few minutes and try again
3. Check your API usage limits

**I can still help with weather, calculations, and search!**"""
            
            elif "quota" in error_msg or "limit" in error_msg or "429" in error_msg:
                return """🤖 API Quota Exceeded

Your Gemini API quota has been exceeded for today.

**Solutions:**
1. Wait until tomorrow for quota reset (most common solution)
2. Get a new API key from [Google AI Studio](https://ai.google.dev)
3. Upgrade your API plan at Google AI Studio

**Other tools still work perfectly:**
- Weather: "weather in [city]"
- Calculator: "calculate 2+2"  
- Search: "search for python"
- Strings: "uppercase 'hello'"
"""
            
            else:
                return f"""🤖 Chat Error: {str(e)}

**Quick fixes:**
1. Check your internet connection
2. Verify your Gemini API key
3. Try again in a few moments

**Other features available:**
- Weather, Calculator, Search, String operations"""

HF_MODEL_URLS = [
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
    "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
    "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
]
HF_API_KEY = os.getenv("HF_API_KEY", st.secrets.get("HF_API_KEY"))

class ImageGenerationTool:
    def __init__(self):
        self.name = "ImageGenerationTool"
        
    def handle_input(self, prompt: str) -> dict:
        if not HF_API_KEY:
            return {"type": "error", "message": "❌ Missing Hugging Face API Key. Set HF_API_KEY in .env file"}
    
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": prompt}
        response = None
    
        for i, model_url in enumerate(HF_MODEL_URLS):
            try:
                response = requests.post(model_url, headers=headers, json=payload, timeout=60)
    
                # ✅ Check if response is image
                if response.status_code == 200 and "image" in response.headers.get("content-type", ""):
                    break
                elif response.status_code in [404, 503]:
                    continue
            except Exception as e:
                print(f"❌ Exception with {model_url}: {e}")
                continue
    
        if response is None or response.status_code != 200 or "image" not in response.headers.get("content-type", ""):
            # Try to parse error
            try:
                err = response.json()
            except:
                err = response.text
            return {
                "type": "error",
                "message": f"❌ Failed to generate image for prompt: {prompt}\nError: {err}"
            }
    
        # ✅ Save image safely
        os.makedirs("images", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"images/generated_{timestamp}.png"
    
        with open(filename, "wb") as f:
            f.write(response.content)
    
        return {
            "type": "image",
            "image_path": filename,
            "message": f"🎨 Generated image for: {prompt}"
        }


class WeatherTool:
    def __init__(self):
        self.name = "WeatherTool"
        print("🌤️ Weather tool initialized with free weather service")
        
    def handle_input(self, query):
        """Handle weather queries using free weather API"""
        try:
            # Extract city from query
            city = self._extract_city(query)
            print(f"🌍 Looking up weather for: {city}")
            
            # Get weather from free API
            result = self._get_weather_free_api(city)
            if result:
                return result
            else:
                return self._get_demo_weather(city)
                
        except Exception as e:
            return f"Weather service error: {str(e)}"
    
    def _get_weather_free_api(self, city):
        """Get weather from free wttr.in API (no key required)"""
        try:
            # Clean city name
            city_clean = city.strip().replace(' ', '+')
            url = f"http://wttr.in/{city_clean}?format=j1"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print(f"🌐 Requesting weather from wttr.in for {city}...")
            response = requests.get(url, headers=headers, timeout=15)
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if data is valid
                if 'current_condition' not in data or not data['current_condition']:
                    print("❌ Invalid response from weather API")
                    return None
                
                current = data['current_condition'][0]
                nearest_area = data.get('nearest_area', [{}])[0]
                
                # Extract weather data
                temp_c = current['temp_C']
                temp_f = current['temp_F']
                feels_like_c = current['FeelsLikeC']
                feels_like_f = current['FeelsLikeF']
                humidity = current['humidity']
                description = current['weatherDesc'][0]['value']
                wind_speed = current['windspeedKmph']
                wind_dir = current['winddir16Point']
                visibility = current['visibility']
                pressure = current['pressure']
                
                # Get location info
                area_name = nearest_area.get('areaName', [{'value': city}])[0]['value']
                country = nearest_area.get('country', [{'value': ''}])[0]['value']
                
                print("✅ Weather data retrieved successfully!")
                
                return f"""🌤️ Current Weather Information:
                    📍 Location: {area_name}{', ' + country if country else ''}
                    🌡️ Temperature: {temp_c}°C ({temp_f}°F)
                    🌡️ Feels Like: {feels_like_c}°C ({feels_like_f}°F)
                    ☁️ Condition: {description}
                    💨 Wind: {wind_speed} km/h {wind_dir}
                    💧 Humidity: {humidity}%
                    👁️ Visibility: {visibility} km
                    🌪️ Pressure: {pressure} mb
                    🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                    """
            
            elif response.status_code == 404:
                return f"❌ City '{city}' not found. Please check the spelling and try again."
            else:
                print(f"❌ Weather API failed with status: {response.status_code}")
                return None
            
        except requests.exceptions.Timeout:
            print("❌ Weather request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ No internet connection")
            return None
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def _get_demo_weather(self, city):
        """Fallback demo weather when API fails"""
        import random
        
        # Realistic weather patterns for different regions
        weather_patterns = [
            ("Sunny", "☀️", 20, 30),
            ("Partly Cloudy", "⛅", 18, 25),
            ("Cloudy", "☁️", 15, 22),
            ("Light Rain", "🌦️", 12, 20),
            ("Clear", "🌤️", 22, 28),
            ("Overcast", "☁️", 16, 21)
        ]
        
        condition, emoji, min_temp, max_temp = random.choice(weather_patterns)
        temp_c = random.randint(min_temp, max_temp)
        temp_f = (temp_c * 9/5) + 32
        feels_like = temp_c + random.randint(-3, 3)
        humidity = random.randint(40, 80)
        wind_speed = random.randint(5, 25)
        wind_dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        wind_dir = random.choice(wind_dirs)
        pressure = random.randint(1000, 1020)
        
        return f"""🌤️ Weather Information (Demo Mode):
        📍 Location: {city}
        🌡️ Temperature: {temp_c}°C ({temp_f:.1f}°F)
        🌡️ Feels Like: {feels_like}°C
        {emoji} Condition: {condition}
        💨 Wind: {wind_speed} km/h {wind_dir}
        💧 Humidity: {humidity}%
        👁️ Visibility: 10 km
        🌪️ Pressure: {pressure} mb
        🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        ⚠️ Demo mode - Weather service temporarily unavailable""" 
    
    def _extract_city(self, query):
        """Extract city name from user query"""
        query_lower = query.lower().strip()
        
        # Remove common weather query prefixes
        prefixes_to_remove = [
            "weather in ", "weather for ", "weather at ",
            "what's the weather in ", "what is the weather in ",
            "how's the weather in ", "how is the weather in ",
            "temperature in ", "temp in ", "climate in ",
            "forecast for ", "current weather in ",
            "weather ", "temperature ", "temp ", "climate "
        ]
        
        for prefix in prefixes_to_remove:
            if query_lower.startswith(prefix):
                query_lower = query_lower[len(prefix):].strip()
                break
        
        # Remove trailing words
        suffixes_to_remove = [" weather", " temperature", " temp", " climate", " today"]
        for suffix in suffixes_to_remove:
            if query_lower.endswith(suffix):
                query_lower = query_lower[:-len(suffix)].strip()
        
        # If nothing left or too short, try pattern matching
        if not query_lower or len(query_lower) < 2:
            # Look for patterns like "in [city]" or "[city] weather"
            patterns = [
                r"(?:in|for|at)\s+([a-zA-Z\s]+?)(?:\s+(?:weather|temperature|temp|climate|today)|$)",
                r"([a-zA-Z\s]+?)\s+(?:weather|temperature|temp|climate)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, query.lower())
                if match:
                    city = match.group(1).strip()
                    if len(city) > 2:
                        return city.title()
            
            # Default fallback
            return "London"
        
        return query_lower.title()

class WebSearchTool:
    def __init__(self):
        self.name = "WebSearchTool"
        
    def handle_input(self, query):
        """Handle web search using simple approach (no dependencies)"""
        try:
            # Clean the search query
            search_query = query.lower()
            for prefix in ["search for", "find", "look up", "search"]:
                search_query = search_query.replace(prefix, "").strip()
            
            if not search_query:
                search_query = query
            
            # Provide search results using multiple sources
            encoded_query = urllib.parse.quote(search_query)
            
            return f"""🔍 Search Results for: '{search_query}'

1. **{search_query.title()} - Wikipedia**
   Find comprehensive information about {search_query} on Wikipedia.
   🔗 https://en.wikipedia.org/wiki/{search_query.replace(' ', '_')}

2. **{search_query.title()} - Google Search**
   Search Google for the latest information and resources.
   🔗 https://www.google.com/search?q={encoded_query}

3. **{search_query.title()} - YouTube**
   Find videos and tutorials related to {search_query}.
   🔗 https://www.youtube.com/results?search_query={encoded_query}

4. **{search_query.title()} - GitHub**
   Find code repositories and projects related to {search_query}.
   🔗 https://github.com/search?q={encoded_query}

5. **{search_query.title()} - Stack Overflow**
   Find programming solutions and discussions.
   🔗 https://stackoverflow.com/search?q={encoded_query}

💡 **Quick Info**: I've provided direct links to popular sources where you can find information about "{search_query}". Click any link to explore further!"""
            
        except Exception as e:
            return f"🔍 Search error: {str(e)}\n\nTry rephrasing your search query."

class CalculatorTool:
    def __init__(self):
        self.name = "CalculatorTool"
        
    def handle_input(self, query):
        """Handle mathematical calculations using basic operations"""
        try:
            # Clean the query
            calc_query = query.lower()
            for prefix in ["calculate", "compute", "solve", "what is", "find"]:
                calc_query = calc_query.replace(prefix, "").strip()
            
            # Handle specific math functions
            if "square root" in calc_query or "sqrt" in calc_query:
                return self._calculate_sqrt(calc_query)
            
            if "factorial" in calc_query:
                return self._calculate_factorial(calc_query)
            
            if "power" in calc_query or "^" in calc_query or "**" in calc_query:
                return self._calculate_power(calc_query)
            
            if "sin" in calc_query or "cos" in calc_query or "tan" in calc_query:
                return self._calculate_trig(calc_query)
            
            if "log" in calc_query:
                return self._calculate_log(calc_query)
            
            # Basic arithmetic
            return self._calculate_basic(calc_query)
            
        except Exception as e:
            return f"🧮 Calculation error: {str(e)}"
    
    def _calculate_basic(self, expression):
        """Handle basic arithmetic operations"""
        try:
            # Clean expression
            expression = expression.replace("x", "*").replace("÷", "/")
            
            # Safety check: only allow numbers and basic operators
            allowed_chars = set('0123456789+-*/().,= ')
            if not all(c in allowed_chars for c in expression.replace(' ', '')):
                return "🧮 Invalid characters in expression. Use only numbers and +, -, *, /, (, )"
            
            # Evaluate
            result = eval(expression)
            return f"🧮 Calculation Result:\n{expression} = {result}"
            
        except:
            return "🧮 Invalid mathematical expression. Please check your input."
    
    def _calculate_sqrt(self, query):
        """Calculate square root"""
        numbers = re.findall(r'\d+\.?\d*', query)
        if numbers:
            num = float(numbers[0])
            if num < 0:
                return "🧮 Cannot calculate square root of negative number"
            result = math.sqrt(num)
            return f"🧮 √{num} = {result:.6f}"
        return "🧮 Please provide a number for square root calculation"
    
    def _calculate_factorial(self, query):
        """Calculate factorial"""
        numbers = re.findall(r'\d+', query)
        if numbers:
            num = int(numbers[0])
            if num < 0:
                return "🧮 Factorial not defined for negative numbers"
            if num > 20:
                return "🧮 Number too large for factorial (max 20)"
            result = math.factorial(num)
            return f"🧮 {num}! = {result}"
        return "🧮 Please provide a number for factorial calculation"
    
    def _calculate_power(self, query):
        """Calculate power"""
        # Look for patterns like "2 power 3" or "2^3" or "2**3"
        power_patterns = [
            r'(\d+\.?\d*)\s*(?:power|to the power of|\^|\*\*)\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*\^\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*\*\*\s*(\d+\.?\d*)'
        ]
        
        for pattern in power_patterns:
            match = re.search(pattern, query)
            if match:
                base = float(match.group(1))
                exponent = float(match.group(2))
                result = pow(base, exponent)
                return f"🧮 {base}^{exponent} = {result}"
        
        return "🧮 Please specify base and exponent (e.g., '2 power 3' or '2^3')"
    
    def _calculate_trig(self, query):
        """Calculate trigonometric functions"""
        numbers = re.findall(r'\d+\.?\d*', query)
        if numbers:
            angle = float(numbers[0])
            radians = math.radians(angle)  # Convert to radians
            
            if "sin" in query:
                result = math.sin(radians)
                return f"🧮 sin({angle}°) = {result:.6f}"
            elif "cos" in query:
                result = math.cos(radians)
                return f"🧮 cos({angle}°) = {result:.6f}"
            elif "tan" in query:
                result = math.tan(radians)
                return f"🧮 tan({angle}°) = {result:.6f}"
        
        return "🧮 Please provide an angle for trigonometric calculation"
    
    def _calculate_log(self, query):
        """Calculate logarithm"""
        numbers = re.findall(r'\d+\.?\d*', query)
        if numbers:
            num = float(numbers[0])
            if num <= 0:
                return "🧮 Logarithm not defined for non-positive numbers"
            
            if "log10" in query or "log 10" in query:
                result = math.log10(num)
                return f"🧮 log₁₀({num}) = {result:.6f}"
            else:
                result = math.log(num)  # Natural log
                return f"🧮 ln({num}) = {result:.6f}"
        
        return "🧮 Please provide a number for logarithm calculation"

class StringTool:
    def __init__(self):
        self.name = "StringTool"
        
    def handle_input(self, query):
        """Handle string operations"""
        try:
            query_lower = query.lower()
            
            # Extract the text to operate on
            text = self._extract_text(query)
            
            if "uppercase" in query_lower or "upper case" in query_lower:
                return f"🔤 Uppercase: {text.upper()}"
            
            elif "lowercase" in query_lower or "lower case" in query_lower:
                return f"🔤 Lowercase: {text.lower()}"
            
            elif "reverse" in query_lower:
                return f"🔤 Reversed: {text[::-1]}"
            
            elif "length" in query_lower or "count" in query_lower:
                return f"🔤 Length: {len(text)} characters"
            
            elif "words" in query_lower:
                words = text.split()
                return f"🔤 Word count: {len(words)} words\nWords: {words}"
            
            elif "capitalize" in query_lower or "title case" in query_lower:
                return f"🔤 Capitalized: {text.title()}"
            
            elif "remove spaces" in query_lower:
                return f"🔤 No spaces: {text.replace(' ', '')}"
            
            elif "replace" in query_lower:
                return self._handle_replace(query, text)
            
            else:
                return f"""🔤 String Operations Available:
📝 Text: "{text}"
- **uppercase/lowercase**: Change case
- **reverse**: Reverse the text
- **length**: Count characters
- **words**: Count words
- **capitalize**: Title case
- **remove spaces**: Remove all spaces
- **replace [old] with [new]**: Replace text

Example: "make 'hello world' uppercase"
"""
                
        except Exception as e:
            return f"🔤 String operation error: {str(e)}"
    
    def _extract_text(self, query):
        """Extract text from query using quotes or common patterns"""
        # Look for text in quotes
        quote_patterns = [
            r"['\"]([^'\"]+)['\"]",
            r"text\s+['\"]([^'\"]+)['\"]",
            r"string\s+['\"]([^'\"]+)['\"]"
        ]
        
        for pattern in quote_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1)
        
        # Look for patterns like "make [text] uppercase"
        operation_patterns = [
            r"make\s+(.+?)\s+(?:uppercase|lowercase|reverse|capitalize)",
            r"(?:uppercase|lowercase|reverse|capitalize)\s+(.+?)(?:\s|$)",
            r"length\s+of\s+(.+?)(?:\s|$)",
            r"count\s+(?:characters|words)\s+in\s+(.+?)(?:\s|$)"
        ]
        
        for pattern in operation_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Default: return the query itself
        return query
    
    def _handle_replace(self, query, text):
        """Handle text replacement"""
        # Look for replace patterns
        patterns = [
            r"replace\s+['\"]([^'\"]+)['\"]\s+with\s+['\"]([^'\"]+)['\"]",
            r"replace\s+(\w+)\s+with\s+(\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                old_text = match.group(1)
                new_text = match.group(2)
                result = text.replace(old_text, new_text)
                return f"🔤 Replaced '{old_text}' with '{new_text}': {result}"
        
        return "🔤 Please specify what to replace and with what. Example: replace 'old' with 'new'"

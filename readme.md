# 🤖 Agentic Conversational Assistant

A powerful Python-based agent system with a Streamlit web interface that intelligently routes user queries to specialized agents for different tasks.

## 🚀 Features

### 🧠 Intelligent Agent Routing
- **ChatTool**: General conversation powered by Google Gemini AI
- **WeatherTool**: Real-time weather information for any city
- **WebSearchTool**: Multi-platform search with direct links to resources
- **CalculatorTool**: Advanced mathematical calculations and operations
- **StringTool**: Text manipulation and string operations

### 🎨 Modern Web Interface
- Clean, responsive Streamlit interface with WhatsApp-inspired design
- Real-time message bubbles with proper alignment
- Chat history export functionality
- Easy-to-use controls and navigation

### 🔧 Smart Query Processing
The system automatically detects query intent and routes to the appropriate agent:
- Weather queries → WeatherTool
- Math operations → CalculatorTool
- Search requests → WebSearchTool
- Text operations → StringTool
- General conversation → ChatTool

## 📁 Project Structure

```
multi_agent/
├── app.py              # Main Streamlit application
├── agents.py           # MasterAgent class with routing logic
├── tools.py            # Individual agent implementations
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API keys)
├── debug_env.py       # Environment debugging utilities
├── test_free_weather.py # Weather API testing
└── readme.md          # Project documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Streamlit
- Google Gemini API key (optional, for chat functionality)

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/ramanakurva164/agentic_chatbot.git
cd multi_agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. **Run the application:**
```bash
streamlit run app.py
```

## 🎯 Usage Examples

### Weather Queries
```
"weather in New York"
"temperature in London"
"forecast for Tokyo"
```

### Mathematical Calculations
```
"calculate 2 + 2"
"square root of 64"
"factorial of 5"
"sin 30 degrees"
```

### Web Search
```
"search for Python tutorials"
"find information about machine learning"
"look up React documentation"
```

### String Operations
```
"make 'hello world' uppercase"
"reverse 'hello'"
"length of 'test string'"
"replace 'old' with 'new' in 'old text'"
```

### General Chat
```
"Hello, how are you?"
"Tell me a joke"
"Explain quantum computing"
```

## 🔧 Technical Details

### Agent Architecture
- **MasterAgent**: Central routing system that analyzes queries and delegates to appropriate tools
- **Modular Design**: Each tool is self-contained and easily extensible
- **Error Handling**: Robust error handling with informative user feedback
- **Fallback Systems**: Demo modes when external APIs are unavailable

### Key Features
- **No-dependency Weather**: Uses free wttr.in API (no API key required)
- **Offline Calculator**: Full mathematical operations without external dependencies
- **Smart Text Processing**: Advanced regex patterns for query parsing
- **Responsive UI**: Custom CSS for optimal user experience

## 🌐 API Integration

### Weather Service
- Primary: wttr.in (free, no API key required)
- Fallback: Demo weather data when service unavailable
- Supports global cities and real-time data

### AI Chat Service
- Google Gemini API for intelligent conversations
- Graceful degradation when API unavailable
- Multiple model fallbacks for reliability

## 📋 Dependencies

```txt
streamlit
google-generativeai
python-dotenv
requests
```

## 🔍 Testing

The repository includes testing utilities:
- `test_free_weather.py`: Weather API functionality testing
- `debug_env.py`: Environment variable debugging

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
The application can be deployed on:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Docker containers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key for chat functionality (optional)

### Adding New Agents
To add a new agent:
1. Create a new class in `tools.py` following the existing pattern
2. Add routing logic in `agents.py`
3. Update the MasterAgent initialization

## 🔒 Privacy & Security

- No user data is stored permanently
- API keys are securely managed through environment variables
- All external API calls include proper error handling
- Chat history is session-based only

## 📊 Performance

- Fast query routing with keyword-based detection
- Lightweight design with minimal dependencies
- Efficient caching for repeated operations
- Responsive UI with real-time updates

## 🐛 Troubleshooting

### Common Issues
1. **Gemini API Error**: Ensure valid API key in `.env` file
2. **Weather Not Loading**: Check internet connection (falls back to demo mode)
3. **Import Errors**: Verify all dependencies are installed

### Debug Mode
Run `debug_env.py` to check environment configuration:
```bash
python debug_env.py
```

## 📞 Support

- **Author**: ramanakurva164
- **Repository**: [multi_agent](https://github.com/ramanakurva164/agentic_chatbot)
- **Issues**: Report bugs via GitHub Issues

## 📄 License

This project is open source. Feel free to use and modify according to your needs.

## 🔮 Future Enhancements

- [ ] File upload and processing capabilities
- [ ] Image analysis integration
- [ ] Database connectivity
- [ ] User authentication system
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

---

**Built with ❤️ using Python, Streamlit, and AI**

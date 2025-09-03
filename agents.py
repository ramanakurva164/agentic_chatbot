import os
import re
from tools import ChatTool, WeatherTool, WebSearchTool, StringTool ,CalculatorTool, ImageGenerationTool

class MasterAgent:
    def __init__(self):
        print("🤖 Initializing Multi-Agent System...")
        
        self.tools = {
            "chat": ChatTool(),
            "weather": WeatherTool(),
            "search": WebSearchTool(),
            "calculator": CalculatorTool(),
            "string": StringTool(),
            "image": ImageGenerationTool()
        }
        self.last_agent_used = "ChatTool"
        print("✅ All agents initialized successfully!")
        
    def route(self, query):
        """Route query to appropriate tool"""
        try:
            if not query or not isinstance(query, str):
                return "Please provide a valid question."
                
            query_lower = query.lower()
            
            # Weather routing
            if any(word in query_lower for word in ["weather", "temperature", "forecast", "climate", "rain", "sunny", "cloudy"]):
                self.last_agent_used = "WeatherTool"
                return self.tools["weather"].handle_input(query)
            
            # Search routing
            elif any(re.search(rf"\b{word}\b", query_lower) for word in ["search", "find", "lookup", "google", "duckduckgo"]):
                self.last_agent_used = "WebSearchTool"
                return self.tools["search"].handle_input(query)
            
            # Calculator routing
            elif any(word in query_lower for word in ["calculate", "math", "solve", "equation", "+", "-", "*", "/", "=", "factorial", "square root", "sqrt", "sin", "cos", "tan", "log", "power", "^"]):
                self.last_agent_used = "CalculatorTool"
                return self.tools["calculator"].handle_input(query)
            
            # String operations routing
            elif any(word in query_lower for word in ["uppercase", "lowercase", "reverse", "length", "count", "capitalize", "replace", "string", "text"]):
                self.last_agent_used = "StringTool"
                return self.tools["string"].handle_input(query)
            elif any(word in query_lower for word in ["image", "picture", "photo", "draw", "create", "generate"]):
                self.last_agent_used = "ImageGenerationTool"
                result = self.tools["image"].handle_input(query)
                if isinstance(result, dict) and result.get("type") == "image":
                    # Return only the image path for display
                    return {
                        "type": "image",
                        "image_path": result.get("image_path"),
                        "message": result.get("message")
                    }
                return result
            # Default to chat
            else:
                self.last_agent_used = "ChatTool"
                return self.tools["chat"].handle_input(query)
                
        except Exception as e:
            return f"Routing error: {str(e)}"

    def handle_user_input(self, query):
        """Alternative method name for compatibility"""
        return self.route(query)

    def get_available_tools(self):
        """Get list of available tools"""
        return list(self.tools.keys())
    
    def get_last_agent(self):
        """Get the name of the last agent used"""
        return self.last_agent_used
    
    def add_tool(self, name, tool_instance):
        """Add a new tool to the system"""
        self.tools[name] = tool_instance
        print(f"✅ Added new tool: {name}")
    
    def remove_tool(self, name):
        """Remove a tool from the system"""
        if name in self.tools:
            del self.tools[name]
            print(f"🗑️ Removed tool: {name}")
        else:
            print(f"❌ Tool '{name}' not found")

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
            
            # Weather routing - more specific patterns
            if any(word in query_lower for word in ["weather", "temperature", "forecast", "climate", "rain", "sunny", "cloudy", "humidity", "wind"]):
                self.last_agent_used = "WeatherTool"
                return self.tools["weather"].handle_input(query)
            
            # Search routing - more specific patterns to avoid false positives
            elif any(re.search(rf"\b{word}\b", query_lower) for word in ["search for", "find information", "lookup", "google", "duckduckgo"]) or \
                 query_lower.startswith(("search ", "find ", "lookup ")):
                self.last_agent_used = "WebSearchTool"
                return self.tools["search"].handle_input(query)
            
            # Calculator routing - more specific math patterns
            elif any(word in query_lower for word in ["calculate", "math", "solve", "equation", "factorial", "square root", "sqrt", "sin", "cos", "tan", "log", "power"]) or \
                 re.search(r'[\d\+\-\*\/\=\^\(\)]+', query_lower):
                self.last_agent_used = "CalculatorTool"
                return self.tools["calculator"].handle_input(query)
            
            # String operations routing - more specific patterns
            elif any(re.search(rf"\b{word}\b", query_lower) for word in ["uppercase", "lowercase", "reverse string", "string length", "count characters", "capitalize", "replace text"]) or \
                 query_lower.startswith(("make uppercase", "make lowercase", "reverse ", "count ", "replace ")):
                self.last_agent_used = "StringTool"
                return self.tools["string"].handle_input(query)
            
            # Image generation routing - more specific patterns
            elif any(re.search(rf"\b{word}\b", query_lower) for word in ["generate image", "create image", "draw picture", "make picture"]) or \
                 query_lower.startswith(("generate ", "create ", "draw ", "make ")):
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
            
            # Default to chat for general conversation
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

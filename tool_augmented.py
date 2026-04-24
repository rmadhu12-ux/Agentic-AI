import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
# New 2026 Import Path
from langchain_classic.agents import initialize_agent, Tool, AgentType

# 1. Setup API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDJt297G2-qlqZyKOP8p3mEhcpCxq2So0g"

# 2. Define the Weather Tool
def get_weather(location_query: str):
    """Fetches current weather for a given city name using Open-Meteo."""
    try:
        # Step A: Get Lat/Long for the city name using a free geocoding service
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_query}&count=1"
        geo_data = requests.get(geo_url).json()
        
        if not geo_data.get("results"):
            return "City not found."
        
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city = geo_data["results"][0]["name"]

        # Step B: Get the weather using those coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()
        
        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data["current_weather"]["windspeed"]
        
        return f"The current weather in {city} is {temp}°C with a wind speed of {wind} km/h."
    except Exception as e:
        return f"Error fetching weather: {e}"
    
# --- TOOL 2: Currency Converter ---
def convert_currency(query: str):
    """
    Converts currency. 
    Input should be 'amount,from_currency,to_currency' (e.g., '100,USD,INR')
    """
    try:
        # The AI will try to provide the input in the format we requested in the description
        amount, from_curr, to_curr = query.split(',')
        amount = float(amount.strip())
        from_curr = from_curr.strip().upper()
        to_curr = to_curr.strip().upper()

        # Using a free, no-key-required public API for exchange rates
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        data = requests.get(url).json()
        
        if data.get("result") == "success":
            rate = data["rates"][to_curr]
            converted_amount = amount * rate
            return f"{amount} {from_curr} is equal to {converted_amount:.2f} {to_curr} (Rate: {rate})"
        else:
            return "Could not fetch exchange rates. Check the currency codes (e.g., USD, CAD, INR)."
    except Exception as e:
        return "Please provide input as 'amount,from_currency,to_currency'. Example: '50,USD,CAD'"    

# 3. Create the Agent
tools = [
    Tool(
        name="Weather_Search",
        func=get_weather,
        description="Useful for when you need to answer questions about the current weather in a specific city."
    ),
    Tool(
        name="Currency_Converter",
        func=convert_currency,
        description="Useful for converting money between currencies. Input MUST be in the format: amount,from_currency,to_currency. Example: 100,USD,INR"
    )
]

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
agent = initialize_agent(
    tools, 
    llm, 
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# 4. Run it
'''print("--- AI Weather Agent ---")
user_input = input("Ask about the weather: ") # Example: "What's the weather in Edmonton?"
response = agent.run(user_input)
print(f"\nFinal Answer: {response}")'''

print("--- Multi-Tool AI Agent ---")
user_input = input("How can I help you today? ") 
# Try: "What is 150 Canadian dollars in Indian Rupees?"
result = agent.invoke({"input": user_input})
print(f"\nFinal Answer: {result['output']}")
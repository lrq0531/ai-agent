from google.genai import types
from google.adk.agents.llm_agent import Agent

# This is the "Meta-Tool" that lets the agent code its own solutions
code_tool = types.Tool(code_execution=types.ToolCodeExecution())


# Mock tool implementation
def get_current_weather(city: str) -> dict:
    """
    Returns the current weather for a city.

    Args:
        city: The full name of the city (e.g., 'London', 'New York').
    """
    return {
        "status": "success",
        "city": city,
        "weather": "Sunny",
        "temperature": "25°C",
    }


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """
    Returns the current time for a city.

    Args:
        city: The full name of the city (e.g., 'London', 'New York').
    """
    return {"status": "success", "city": city, "time": "10:30 AM"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Tells the current time and weather in a specified city.",
    instruction=(
        "You are a helpful and creative assistant.\n"
        "- Use 'get_current_time' when the user asks for the time.\n"
        "- Use 'get_current_weather' when the user asks for the weather.\n"
        "If the user asks for both, call the tools sequentially."
    ),
    tools=[get_current_time, get_current_weather],
)

from google.genai import types
from google.adk.agents.llm_agent import Agent

# This is the "Meta-Tool" that lets the agent code its own solutions
code_tool = types.Tool(code_execution=types.ToolCodeExecution())

root_agent = Agent(
    model='gemini-2.5-flash', # Gemini 2.0+ is optimized for this
    name='creative_agent',
    instruction="""You are a creative assistant. 
    If a user asks for data you don't have a tool for, write and run 
    Python code to find or calculate that information. 
    For example, if asked about currency levels at a beach, 
    write code to fetch current exchange rates and local prices.""",
    tools=[code_tool] # The agent now has the 'power' to create logic
)
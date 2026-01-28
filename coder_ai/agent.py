import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types, Client

# Use a stable Image ID for the SDK
IMAGE_MODEL = "imagen-4.0-generate-001"


# --- Custom Image Tool ---
async def generate_news_visual(prompt: str):
    """Generates a visual summary or illustration for a news topic.
    Args:
        prompt: A detailed description of the image to generate.
    """
    client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = client.models.generate_images(
        model=IMAGE_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1),
    )

    # In a real app, you'd save this to the ADK Artifact service.
    # For now, we'll return a confirmation string.
    if response.generated_images:
        # Save locally to view it
        image_path = "latest_news_visual.png"
        response.generated_images[0].image.save(image_path)
        return f"[Image Generated: {image_path}]"
    return "Failed to generate image."


# --- Updated Agent ---
root_agent = Agent(
    name="news_visualizer_agent",
    model="gemini-2.5-flash",
    description="Searches for news and creates a visual summary.",
    instruction="""
    1. First, use 'google_search' to find the latest information requested.
    2. Then, create a descriptive prompt and use the 'generate_news_visual' tool 
       to create an image that represents the news.
    3. Provide a text summary and confirm the image has been created.
    """,
    tools=[google_search, generate_news_visual],  # Added the new tool here
)


# --- Updated Runner Logic ---
async def call_agent_async(query):
    # (Existing setup code remains the same)
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, app_name="visual_agent", session_service=session_service
    )

    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run_async(
        user_id="user123", session_id="sess123", new_message=content
    )

    async for event in events:
        # This will now show the tool calls as they happen!
        if event.is_final_response():
            print("\nAgent Answer:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(call_agent_async("What is the latest news about NASA's Moon mission?"))

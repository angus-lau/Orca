import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Check if the key was loaded
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize the client
client = OpenAI(api_key=api_key)

# Make a simple call to OpenAI's chat model
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "yO wassup dudeee"}
        ]
    )
    print("✅ OpenAI API key is working!")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("❌ Failed to connect to OpenAI API.")
    print(e)
